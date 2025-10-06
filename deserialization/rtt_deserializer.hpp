#pragma once

#include <string>

#include <rtt_metrics/rtt_metrics_type.hpp>
#include <rtt_metrics/accel_metrics.hpp>
#include <accelerometer/common_structs.hpp>

rtt_metrics::MetricType deserialize_rtt_metrics(const std::string &data);