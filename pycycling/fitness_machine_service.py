"""
Interact with a Fitness Machine Service (FTMS) Bluetooth LE device.

Example
=======
This example demonstrates all cycling-related functionalities of a FTMS indoor cycling device.

Please see also information on :ref:`obtaining the Bluetooth address of your device <obtaining_device_address>`.

First, it prints all 'read' characteristics:
    + Supported resistance level range
    + Supported power range
    + Fitness machine features

Then, it starts 'notify' characteristics, which stream data from the device:
    + Indoor bike data (speed, cadence, distance, resistance level, power, time)

Finally, it modifies 'write' characteristics with some time in between:
    + Resistance level
    + Target power (automatically adjusts resistance level based on cadence to maintain same power)

.. literalinclude:: ../examples/fitness_machine_service_example.py

"""
from collections import namedtuple

from pycycling.ftms_parsers import (
    parse_fitness_machine_status,
    parse_indoor_bike_data,
    parse_fitness_machine_feature,
    parse_training_status,
    parse_control_point_response,
    form_ftms_control_command,
    FTMSControlPointOpCode,
    FitnessMachineFeature,
)

# read: Supported Resistance Level Range
ftms_supported_resistance_level_range_characteristic_id = (
    "00002ad6-0000-1000-8000-00805f9b34fb"
)
# read: Supported Power Range
ftms_supported_power_range_characteristic_id = "00002ad8-0000-1000-8000-00805f9b34fb"
# (read): Fitness Machine Feature
ftms_fitness_machine_feature_characteristic_id = "00002acc-0000-1000-8000-00805f9b34fb"
# notify: Indoor Bike Data
ftms_indoor_bike_data_characteristic_id = "00002ad2-0000-1000-8000-00805f9b34fb"
# notify: Fitness Machine Status
ftms_fitness_machine_status_characteristic_id = "00002ada-0000-1000-8000-00805f9b34fb"
# notify: Training Status
ftms_training_status_characteristic_id = "00002ad3-0000-1000-8000-00805f9b34fb"
# (write, indicate): Fitness Machine Control Point
ftms_fitness_machine_control_point_characteristic_id = (
    "00002ad9-0000-1000-8000-00805f9b34fb"
)

SupportedResistanceLevelRange = namedtuple(
    "SupportedResistanceLevelRange",
    ["minimum_resistance", "maximum_resistance", "minimum_increment"],
)


def _parse_supported_resistance_level_range(message: bytearray) -> SupportedResistanceLevelRange:
    minimum_resistance = int.from_bytes(message[0:2], "little")
    maximum_resistance = int.from_bytes(message[2:4], "little")
    minimum_increment = int.from_bytes(message[4:6], "little")
    return SupportedResistanceLevelRange(
        minimum_resistance, maximum_resistance, minimum_increment
    )


SupportedPowerRange = namedtuple(
    "SupportedPowerRange",
    ["minimum_power", "maximum_power", "minimum_increment"],
)


def _parse_supported_power_range(message: bytearray) -> SupportedPowerRange:
    minimum_power = int.from_bytes(message[0:2], "little")
    maximum_power = int.from_bytes(message[2:4], "little")
    minimum_increment = int.from_bytes(message[4:6], "little")
    return SupportedPowerRange(minimum_power, maximum_power, minimum_increment)


class FitnessMachineService:
    def __init__(self, client):
        self._client = client
        self._control_point_response_callback = None
        self._indoor_bike_data_callback = None
        self._fitness_machine_status_callback = None
        self._training_status_callback = None

    # === READ Characteristics ===
    async def get_supported_resistance_level_range(self) -> SupportedResistanceLevelRange:
        message = await self._client.read_gatt_char(
            ftms_supported_resistance_level_range_characteristic_id
        )
        return _parse_supported_resistance_level_range(message)

    async def get_supported_power_range(self) -> SupportedPowerRange:
        message = await self._client.read_gatt_char(
            ftms_supported_power_range_characteristic_id
        )
        return _parse_supported_power_range(message)

    async def get_fitness_machine_feature(self) -> FitnessMachineFeature:
        message = await self._client.read_gatt_char(
            ftms_fitness_machine_feature_characteristic_id
        )
        return parse_fitness_machine_feature(message)

    # === NOTIFY Characteristics ===
    # ====== Indoor Bike Data ======
    async def enable_indoor_bike_data_notify(self) -> None:
        await self._client.start_notify(
            ftms_indoor_bike_data_characteristic_id,
            self._indoor_bike_data_notification_handler,
        )

    async def disable_indoor_bike_data_notify(self):
        await self._client.stop_notify(ftms_indoor_bike_data_characteristic_id)

    def set_indoor_bike_data_handler(self, callback):
        self._indoor_bike_data_callback = callback

    def _indoor_bike_data_notification_handler(
        self, sender, data
    ):  # pylint: disable=unused-argument
        if self._indoor_bike_data_callback is not None:
            self._indoor_bike_data_callback(parse_indoor_bike_data(data))

    # ====== Fitness Machine Status ======
    async def enable_fitness_machine_status_notify(self) -> None:
        await self._client.start_notify(
            ftms_fitness_machine_status_characteristic_id,
            self._fitness_machine_status_notification_handler,
        )

    async def disable_fitness_machine_status_notify(self):
        await self._client.stop_notify(ftms_fitness_machine_status_characteristic_id)

    def set_fitness_machine_status_handler(self, callback):
        self._fitness_machine_status_callback = callback

    def _fitness_machine_status_notification_handler(
        self, sender, data
    ):  # pylint: disable=unused-argument
        if self._fitness_machine_status_callback is not None:
            self._fitness_machine_status_callback(parse_fitness_machine_status(data))

    # ====== Training Status ======
    async def enable_training_status_notify(self) -> None:
        await self._client.start_notify(
            ftms_training_status_characteristic_id,
            self._training_status_notification_handler,
        )

    async def disable_training_status_notify(self):
        await self._client.stop_notify(ftms_training_status_characteristic_id)

    def set_training_status_handler(self, callback):
        self._training_status_callback = callback

    def _training_status_notification_handler(
        self, sender, data
    ):  # pylint: disable=unused-argument
        if self._training_status_callback is not None:
            self._training_status_callback(parse_training_status(data))

    # === WRITE/INDICATE Characteristics ===
    # ====== Fitness Machine Control Point ======
    async def enable_control_point_indicate(self) -> None:
        await self._client.start_notify(
            ftms_fitness_machine_control_point_characteristic_id,
            self._control_point_response_handler,
        )

    async def disable_control_point_indicate(self):
        await self._client.stop_notify(
            ftms_fitness_machine_control_point_characteristic_id
        )

    def set_control_point_response_handler(self, callback):
        self._control_point_response_callback = callback

    def _control_point_response_handler(
        self, sender, data
    ):  # pylint: disable=unused-argument
        if self._control_point_response_callback is not None:
            self._control_point_response_callback(parse_control_point_response(data))

    async def request_control(self) -> None:
        message = form_ftms_control_command(FTMSControlPointOpCode.REQUEST_CONTROL)
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def reset(self) -> None:
        message = form_ftms_control_command(FTMSControlPointOpCode.RESET)
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_target_resistance_level(self, level: int) -> None:
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGET_RESISTANCE_LEVEL, int(level)
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_target_power(self, power: int) -> None:
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGET_POWER, int(power)
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )
