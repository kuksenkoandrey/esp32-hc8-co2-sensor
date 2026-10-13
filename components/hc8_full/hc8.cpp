#include "hc8.h"
#include "esphome/core/log.h"

namespace esphome {
namespace hc8_full {

static const char *const TAG = "hc8_full";
static const uint8_t HEADER[2] = {0x42, 0x4D};

void HC8FullComponent::update() {
  if (!this->read_data_()) {
    ESP_LOGW(TAG, "No valid data from HC8");
  }
}

void HC8FullComponent::loop() {
  while (this->available() >= 16) {
    uint8_t data[16];
    if (!this->read_array(data, 16)) {
      break;
    }
    if (data[0] == HEADER[0] && data[1] == HEADER[1]) {
      this->parse_data_(data);
    } else {
      break;
    }
  }
}

bool HC8FullComponent::read_data_() {
  if (this->available() < 16)
    return false;

  uint8_t data[16];
  if (!this->read_array(data, 16))
    return false;

  if (data[0] != HEADER[0] || data[1] != HEADER[1])
    return false;

  uint16_t sum = 0x42 + 0x4D;
  for (int i = 2; i < 15; i++) sum += data[i];
  if ((uint8_t)(sum & 0xFF) != data[15])
    return false;

  this->parse_data_(data);
  return true;
}

void HC8FullComponent::parse_data_(const uint8_t *data) {
  uint16_t voc  = (data[2] << 8) | data[3];
  float temp = ((data[4] << 8) | data[5]) / 100.0f;
  uint16_t co2  = (data[6] << 8) | data[7];
  float hum  = ((data[8] << 8) | data[9]) / 10.0f;

  ESP_LOGD(TAG, "CO2=%d ppm, VOC=%d ug/m3, Temp=%.1f C, Hum=%.1f %%", co2, voc, temp, hum);

  if (co2_sensor_ != nullptr) co2_sensor_->publish_state(co2);
  if (voc_sensor_ != nullptr) voc_sensor_->publish_state(voc);
  if (temperature_sensor_ != nullptr) temperature_sensor_->publish_state(temp);
  if (humidity_sensor_ != nullptr) humidity_sensor_->publish_state(hum);
}

}  // namespace hc8_full
}  // namespace esphome