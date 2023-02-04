from enum import Enum
from collections import namedtuple

FitnessMachineStatusMessage = namedtuple("FitnessMachineStatusMessage", [
    "status",
    "value",
    "unit",
])


class FitnessMachineStatus(Enum):
    RESERVED_FOR_FUTURE_USE = 0
    RESET = 1
    STOPPED_BY_USER = 2
    PAUSED_BY_USER = 3
    STOPPED_BY_SAFETY_KEY = 4
    STARTED_BY_USER = 5
    NEW_SPEED = 6
    NEW_INCLINATION = 7
    NEW_RESISTANCE = 8
    NEW_POWER = 9
    NEW_HEART_RATE = 10
    NEW_EXPENDED_ENERGY = 11
    NEW_NUMBER_OF_STEPS = 12
    NEW_NUMBER_OF_STRIDES = 13
    NEW_DISTANCE = 14
    NEW_TRAINING_TIME = 15
    NEW_TWO_HEART_RATE_ZONE_TARGET_TIME = 16
    NEW_THREE_HEART_RATE_ZONE_TARGET_TIME = 17
    NEW_FIVE_HEART_RATE_ZONE_TARGET_TIME = 18
    NEW_INDOOR_BIKE_SIMULATION_PARAMETERS = 19
    NEW_WHEEL_CIRCUMFERENCE = 20
    NEW_SPIN_DOWN_STATUS = 21
    NEW_TARGET_CADENCE = 22
    CONTROL_PERMISSION_LOST = 23


TwoZoneHR = namedtuple(
    "TwoZoneHR",
    [
        "fat_burn",
        "fitness",
    ],
)

ThreeZoneHR = namedtuple(
    "ThreeZoneHR",
    [
        "very_light",
        "light",
        "moderate",
    ],
)

FiveZoneHR = namedtuple(
    "FiveZoneHR",
    [
        "very_light",
        "light",
        "moderate",
        "hard",
        "maximum",
    ],
)

IndoorBikeSimulationParameters = namedtuple(
    "IndoorBikeSimulationParameters",
    [
        "wind_speed",
        "grade",
        "coefficient_of_rolling_resistance",
        "wind_resistance_coefficient",
    ],
)


class SpinDownStatusValue(Enum):
    RESERVED_FOR_FUTURE_USE = 0x00
    SPIN_DOWN_REQUESTED = 0x01
    SUCCESS = 0x02
    ERROR = 0x03
    STOP_PEDALING = 0x04


def parse_fitness_machine_status(message: bytearray) -> FitnessMachineStatusMessage:
    """
    A tuple with three items:
    1. A FitnessMachineStatus enum
    2. Associated data (dictionary or namedtuple())
    3. Units
    """
    parsed_status = (None, None, None)
    if message[0] == 0x00:
        parsed_status = (FitnessMachineStatus.RESERVED_FOR_FUTURE_USE, None, None)
    elif message[0] == 0x01:
        parsed_status = (FitnessMachineStatus.RESET, None, None)
    elif message[0] == 0x02:
        if message[1] == 0x01:
            parsed_status = (FitnessMachineStatus.STOPPED_BY_USER, None, None)
        elif message[1] == 0x02:
            parsed_status = (FitnessMachineStatus.PAUSED_BY_USER, None, None)
        else:
            parsed_status = (FitnessMachineStatus.RESERVED_FOR_FUTURE_USE, None, None)
    elif message[0] == 0x03:
        parsed_status = (FitnessMachineStatus.STOPPED_BY_SAFETY_KEY, None, None)
    elif message[0] == 0x04:
        parsed_status = (FitnessMachineStatus.STARTED_BY_USER, None, None)
    elif message[0] == 0x05:
        speed = int.from_bytes(message[1:3], byteorder="little", signed=False) / 100
        parsed_status = (FitnessMachineStatus.NEW_SPEED, speed, "km/h")
    elif message[0] == 0x06:
        inclination = int.from_bytes(message[1:3], byteorder="little", signed=True) / 10
        parsed_status = (FitnessMachineStatus.NEW_INCLINATION, inclination, "%")
    elif message[0] == 0x07:
        resistance_level = int.from_bytes(message[1:3], byteorder="little", signed=True)
        parsed_status = (FitnessMachineStatus.NEW_RESISTANCE, resistance_level, "%")
    elif message[0] == 0x08:
        power = int.from_bytes(message[1:3], byteorder="little", signed=True)
        parsed_status = (FitnessMachineStatus.NEW_POWER, power, "W")
    elif message[0] == 0x09:
        heart_rate = int.from_bytes(message[1], byteorder="little", signed=False)
        parsed_status = (FitnessMachineStatus.NEW_HEART_RATE, heart_rate, "bpm")
    elif message[0] == 0x0A:
        expended_energy = int.from_bytes(message[1:3], byteorder="little", signed=False)
        parsed_status = (
            FitnessMachineStatus.NEW_EXPENDED_ENERGY,
            expended_energy,
            "kcal",
        )
    elif message[0] == 0x0B:
        number_of_steps = int.from_bytes(message[1:3], byteorder="little", signed=False)
        parsed_status = (
            FitnessMachineStatus.NEW_NUMBER_OF_STEPS,
            number_of_steps,
            "steps",
        )
    elif message[0] == 0x0C:
        number_of_strides = int.from_bytes(
            message[1:3], byteorder="little", signed=False
        )
        parsed_status = (
            FitnessMachineStatus.NEW_NUMBER_OF_STRIDES,
            number_of_strides,
            "strides",
        )
    elif message[0] == 0x0D:
        distance = int.from_bytes(message[1:4], byteorder="little", signed=False)
        parsed_status = (FitnessMachineStatus.NEW_DISTANCE, distance, "m")
    elif message[0] == 0x0E:
        training_time = int.from_bytes(message[1:3], byteorder="little", signed=False)
        parsed_status = (FitnessMachineStatus.NEW_TRAINING_TIME, training_time, "s")
    elif message[0] == 0x0F:
        parameter = TwoZoneHR(
            fat_burn=int.from_bytes(message[1:3], byteorder="little", signed=False),
            fitness=int.from_bytes(message[3:5], byteorder="little", signed=False),
        )
        parsed_status = (
            FitnessMachineStatus.NEW_TWO_HEART_RATE_ZONE_TARGET_TIME,
            parameter,
            "bpm",
        )
    elif message[0] == 0x10:
        parameter = ThreeZoneHR(
            very_light=int.from_bytes(message[1:3], byteorder="little", signed=False),
            light=int.from_bytes(message[3:5], byteorder="little", signed=False),
            moderate=int.from_bytes(message[5:7], byteorder="little", signed=False),
        )
        parsed_status = (
            FitnessMachineStatus.NEW_THREE_HEART_RATE_ZONE_TARGET_TIME,
            parameter,
            "bpm",
        )
    elif message[0] == 0x11:
        parameter = FiveZoneHR(
            very_light=int.from_bytes(message[1:3], byteorder="little", signed=False),
            light=int.from_bytes(message[3:5], byteorder="little", signed=False),
            moderate=int.from_bytes(message[5:7], byteorder="little", signed=False),
            hard=int.from_bytes(message[7:9], byteorder="little", signed=False),
            maximum=int.from_bytes(message[9:11], byteorder="little", signed=False),
        )
        parsed_status = (
            FitnessMachineStatus.NEW_FIVE_HEART_RATE_ZONE_TARGET_TIME,
            parameter,
            "bpm",
        )
    elif message[0] == 0x12:
        parameter = IndoorBikeSimulationParameters(
            wind_speed=int.from_bytes(message[1:3], byteorder="little", signed=False) / 1000,
            grade=int.from_bytes(message[3:5], byteorder="little", signed=False) / 100,
            coefficient_of_rolling_resistance=int.from_bytes(
                message[5:6], byteorder="little", signed=False
            ) / 1000,
            wind_resistance_coefficient=int.from_bytes(
                message[6:7], byteorder="little", signed=False
            ) / 100,
        )
        parsed_status = (
            FitnessMachineStatus.NEW_INDOOR_BIKE_SIMULATION_PARAMETERS,
            parameter,
            "m/s, %, unitless, kg/m",
        )
    elif message[0] == 0x13:
        wheel_circumference = int.from_bytes(
            message[1:3], byteorder="little", signed=False
        )
        parsed_status = (
            FitnessMachineStatus.NEW_WHEEL_CIRCUMFERENCE,
            wheel_circumference,
            "m",
        )
    elif message[0] == 0x14:
        spin_down_status = int.from_bytes(
            message[1:2], byteorder="little", signed=False
        )
        parsed_status = (
            FitnessMachineStatus.NEW_SPIN_DOWN_STATUS,
            SpinDownStatusValue(spin_down_status),
            "unitless",
        )
    elif message[0] == 0x15:
        target_cadence = int.from_bytes(message[1:3], byteorder="little", signed=False)
        parsed_status = (FitnessMachineStatus.NEW_TARGET_CADENCE, target_cadence, "rpm")
    elif message[0] == 0xFF:
        parsed_status = (FitnessMachineStatus.CONTROL_PERMISSION_LOST, None, None)
    return FitnessMachineStatusMessage(
        status=parsed_status[0],
        value=parsed_status[1],
        unit=parsed_status[2],
    )
