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
    parse_all_features,
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


def _parse_supported_resistance_level_range(
    message: bytearray,
) -> SupportedResistanceLevelRange:
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
    async def get_supported_resistance_level_range(
        self,
    ) -> SupportedResistanceLevelRange:
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
        return parse_all_features(message)

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

    # ====== Control Point Commands ======
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

    async def set_target_speed(self, speed: int) -> None:
        if speed < 0:
            raise ValueError("Speed must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGET_SPEED, speed
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_target_incline(self, inclination: int) -> None:
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGET_INCLINE, inclination
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_target_resistance_level(self, level: int) -> None:
        if level < 0:
            raise ValueError("Resistance level must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGET_RESISTANCE_LEVEL, level
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_target_power(self, power: int) -> None:
        if power < 0:
            raise ValueError("Power must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGET_POWER, power
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_target_heart_rate(self, heart_rate: int) -> None:
        if heart_rate < 0:
            raise ValueError("Heart rate must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGET_HEART_RATE, heart_rate
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def start_or_resume(self) -> None:
        message = form_ftms_control_command(FTMSControlPointOpCode.START_OR_RESUME)
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def stop_or_pause(self, pause: bool) -> None:
        message = form_ftms_control_command(
            FTMSControlPointOpCode.STOP_OR_PAUSE, 0x02 if pause else 0x01
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_targeted_expended_energy(self, energy: int) -> None:
        if energy < 0:
            raise ValueError("Energy must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGETED_EXPENDED_ENERGY, energy
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_targeted_number_of_steps(self, steps: int) -> None:
        if steps < 0:
            raise ValueError("Steps must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGETED_NUMBER_OF_STEPS, steps
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_targeted_number_of_strides(self, strides: int) -> None:
        if strides < 0:
            raise ValueError("Strides must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGETED_NUMBER_OF_STRIDES, strides
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_targeted_distance(self, distance: int) -> None:
        if distance < 0:
            raise ValueError("Distance must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGETED_DISTANCE, distance
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_targeted_training_time(self, time: int) -> None:
        if time < 0:
            raise ValueError("Time must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGETED_TRAINING_TIME, time
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_targeted_time_in_two_heart_rate_zones(self, times: list) -> None:
        if len(times) != 2:
            raise ValueError("Times must be a list of 2 elements")
        if times[0] < 0 or times[1] < 0:
            raise ValueError("Times must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGETED_TIME_IN_TWO_HEART_RATE_ZONES, times
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_targeted_time_in_three_heart_rate_zones(self, times: list) -> None:
        if len(times) != 3:
            raise ValueError("Times must be a list of 3 elements")
        if times[0] < 0 or times[1] < 0 or times[2] < 0:
            raise ValueError("Times must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGETED_TIME_IN_THREE_HEART_RATE_ZONES, times
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_targeted_time_in_five_heart_rate_zones(self, times: list) -> None:
        if len(times) != 5:
            raise ValueError("Times must be a list of 5 elements")
        if times[0] < 0 or times[1] < 0 or times[2] < 0 or times[3] < 0 or times[4] < 0:
            raise ValueError("Times must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGETED_TIME_IN_FIVE_HEART_RATE_ZONES, times
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_simulation_parameters(
        self, wind_speed: int, grade: int, crr: int, cw: int
    ) -> None:
        if crr < 0:
            raise ValueError("Crr must be non-negative")
        if cw < 0:
            raise ValueError("Cw must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_INDOOR_BIKE_SIMULATION_PARAMETERS,
            [wind_speed, grade, crr, cw],
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_wheel_circumference(self, circumference: int) -> None:
        if circumference < 0:
            raise ValueError("Circumference must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_WHEEL_CIRCUMFERENCE, circumference
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_spin_down_control(self, control: int) -> None:
        if control < 0:
            raise ValueError("Control must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_SPIN_DOWN_CONTROL, control
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )

    async def set_targeted_cadence(self, cadence: int) -> None:
        if cadence < 0:
            raise ValueError("Cadence must be non-negative")
        message = form_ftms_control_command(
            FTMSControlPointOpCode.SET_TARGETED_CADENCE, cadence
        )
        await self._client.write_gatt_char(
            ftms_fitness_machine_control_point_characteristic_id, message, True
        )
