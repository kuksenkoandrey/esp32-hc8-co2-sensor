import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_CARBON_DIOXIDE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_HUMIDITY,
    STATE_CLASS_MEASUREMENT,
    UNIT_PARTS_PER_MILLION,
    UNIT_CELSIUS,
    UNIT_PERCENT,
    ICON_MOLECULE_CO2,
    ICON_THERMOMETER,
    ICON_WATER_PERCENT,
)

DEPENDENCIES = ["uart"]

hc8_full_ns = cg.esphome_ns.namespace("hc8_full")
HC8FullComponent = hc8_full_ns.class_("HC8FullComponent", cg.PollingComponent, uart.UARTDevice)

CONF_CO2 = "co2"
CONF_VOC = "voc"
CONF_TEMPERATURE = "temperature"
CONF_HUMIDITY = "humidity"

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(HC8FullComponent),
            cv.Optional(CONF_CO2): sensor.sensor_schema(
                unit_of_measurement=UNIT_PARTS_PER_MILLION,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_CARBON_DIOXIDE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon=ICON_MOLECULE_CO2,
            ),
            cv.Optional(CONF_VOC): sensor.sensor_schema(
                unit_of_measurement="µg/m³",
                accuracy_decimals=0,
                device_class="volatile_organic_compounds",
                state_class=STATE_CLASS_MEASUREMENT,
                icon="mdi:air-filter",
            ),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon=ICON_THERMOMETER,
            ),
            cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_HUMIDITY,
                state_class=STATE_CLASS_MEASUREMENT,
                icon=ICON_WATER_PERCENT,
            ),
        }
    )
    .extend(uart.UART_DEVICE_SCHEMA)
    .extend(cv.polling_component_schema("60s"))
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_CO2 in config:
        sens = await sensor.new_sensor(config[CONF_CO2])
        cg.add(var.set_co2_sensor(sens))
    if CONF_VOC in config:
        sens = await sensor.new_sensor(config[CONF_VOC])
        cg.add(var.set_voc_sensor(sens))
    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(sens))
    if CONF_HUMIDITY in config:
        sens = await sensor.new_sensor(config[CONF_HUMIDITY])
        cg.add(var.set_humidity_sensor(sens))