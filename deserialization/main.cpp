#include "accelerometer/common_structs.hpp"
#include <pybind11/pybind11.h>

#include "rtt_deserializer.hpp"

namespace py = pybind11;

PYBIND11_MODULE(RTTMetricsDeserializer, ra, py::mod_gil_not_used()) {
    py::class_<accelerometer::RawAcceleration>(ra, "RawAcceleration")
        .def(py::init<>())
        .def("__repr__", [](const accelerometer::RawAcceleration &self) {
            return "<RawAcceleration x=" + std::to_string(self.val[0]) + " y=" + std::to_string(self.val[1]) + " z=" + std::to_string(self.val[2]) + ">";
        });
    
    ra.def("deserialize", &deserialize_rtt_metrics, "Deserialize RTT metrics data");
}