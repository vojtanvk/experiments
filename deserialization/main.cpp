#include <cassert>
#include <ios>
#include <pybind11/pybind11.h>

#include "rtt_deserializer.hpp"
#include "rtt_metrics/rtt_metrics_type.hpp"

#include <accelerometer/common_structs.hpp>

#include <iostream>
#include <stdio.h>

namespace py = pybind11;


static std::vector<uint8_t> current_data;
static constexpr size_t HEADER_SIZE = 1 + 4;


void deserialize_packet_py(py::buffer b) {
    py::buffer_info info = b.request();

    if (info.ndim != 1)
        throw std::runtime_error("Expected a 1D buffer");

    current_data.clear();

    auto* data = static_cast<const uint8_t*>(info.ptr);
    size_t size = static_cast<size_t>(info.size);

    current_data.clear();
    current_data.reserve(size);

    deserialize_packet(data, size, current_data);
    // for(auto a : current_data) {    
    //     printf("%02X\n",a);
    // }
    
}

accelerometer::RawAcceleration read_raw_acceleration() {
    static constexpr size_t DATA_SIZE = 6;
    assert(current_data.size() == HEADER_SIZE + DATA_SIZE);
    
    std::vector<uint8_t> buffer;
    for(size_t i=HEADER_SIZE; i<current_data.size(); ++i) {
        buffer.push_back(current_data[i]);
    }

    accelerometer::RawAcceleration res = deserialize_raw_acceleration(buffer);
    return res;
}

rtt_metrics::MetricType get_type() {
    assert(!current_data.empty());
    return rtt_metrics::MetricType{current_data.front()};
}

uint32_t get_timestamp() {
    assert(current_data.size() >= 5);
    return (current_data[1] << 24) + (current_data[2] << 16) + (current_data[3] << 8) + (current_data[4]);
}

PYBIND11_MODULE(RTTMetricsDeserializer, ra, py::mod_gil_not_used()) {
    py::class_<accelerometer::RawAcceleration>(ra, "RawAccelerationData")
        .def(py::init<>())
        .def_property("x",
        [](const accelerometer::RawAcceleration &self) { return self.val[0]; },
        [](accelerometer::RawAcceleration &self, float v) { self.val[0] = v; })
        .def_property("y",
        [](const accelerometer::RawAcceleration &self) { return self.val[1]; },
        [](accelerometer::RawAcceleration &self, float v) { self.val[1] = v; })
        .def_property("z",
        [](const accelerometer::RawAcceleration &self) { return self.val[2]; },
        [](accelerometer::RawAcceleration &self, float v) { self.val[2] = v; })
        .def("__repr__", [](const accelerometer::RawAcceleration &self) {
            return "<RawAcceleration x=" + std::to_string(self.val[0]) + " y=" + std::to_string(self.val[1]) + " z=" + std::to_string(self.val[2]) + ">";
        });
    
    py::enum_<rtt_metrics::MetricType>(ra, "MetricType")
        .value("RawAcceleration", rtt_metrics::MetricType::RawAcceleration)
        .value("RawAccelerationError", rtt_metrics::MetricType::RawAccelerationError)
        .value("cnt_", rtt_metrics::MetricType::cnt_)
        .export_values();

    ra.def("deserialize", &deserialize_packet_py, "Deserialize RTT metrics packet");
    ra.def("get_type", &get_type, "Get type of currently deserialized packet");
    ra.def("read_raw_acceleration", &read_raw_acceleration, "Read RawAcceleration data from currently deserialized packet");
    ra.def("get_timestamp", &get_timestamp, "Get timestamp of currently deserialized packet");
}