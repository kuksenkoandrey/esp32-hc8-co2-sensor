#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/uart/uart.h"

namespace esphome {
namespace hc8_full {

class HC8FullComponent : public PollingComponent, public uart::UARTDevice {
 public:
  void set_co2_sensor(sensor::Sensor *s) { co2_sensor_ = s; }
  void set_voc_sensor(sensor::Sensor *s) { voc_sensor_ = s; }
  void set_temperature_sensor(sensor::Sensor *s) { temperature_sensor_ = s; }
  void set_humidity_sensor(sensor::Sensor *s) { humidity_sensor_ = s; }

  void update() override;
  void loop() override;

 protected:
  bool read_data_();
  void parse_data_(const uint8_t *data);

  sensor::Sensor *co2_sensor_{nullptr};
  sensor::Sensor *voc_sensor_{nullptr};
  sensor::Sensor *temperature_sensor_{nullptr};
  sensor::Sensor *humidity_sensor_{nullptr};
};

}  // namespace hc8_full
}  // namespace esphome