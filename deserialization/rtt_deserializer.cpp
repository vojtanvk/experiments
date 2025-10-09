#include "rtt_deserializer.hpp"
#include "accelerometer/common_structs.hpp"
#include "bitsery/include/bitsery/deserializer.h"
#include <cobs/cobs.hpp>

#include <iostream>
#include <stdio.h>

#include <bitsery/bitsery.h>
#include <cstdint>
#include <utility>


using namespace rtt_metrics;

void deserialize_packet(const uint8_t*data, const size_t data_size, std::vector<uint8_t> &out) {
    uint8_t buffer[256];
    auto decoded_size = cobs::decode(data, data_size, buffer, 256);
    assert(decoded_size.has_value());
    for(size_t i=0; i<decoded_size.value(); ++i) {
        out.push_back(buffer[i]);
    }
}


accelerometer::RawAcceleration deserialize_raw_acceleration(const std::vector<uint8_t> data) {
    accelerometer::RawAcceleration res;
    auto state = bitsery::quickDeserialization<InputAdapter>({data.begin(), data.size()}, res);

    assert(state.first == bitsery::ReaderError::NoError && state.second);

    return res;
}