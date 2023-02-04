from collections import namedtuple
from enum import Enum


class TrainingStatus(Enum):
    OTHER = 0
    IDLE = 1
    WARMING_UP = 2
    LOW_INTENSITY_INTERVAL = 3
    HIGH_INTENSITY_INTERVAL = 4
    RECOVERY_INTERVAL = 5
    ISOMETRIC = 6
    HEART_RATE_CONTROL = 7
    FITNESS_TEST = 8
    SPEED_OUTSIDE_CONTROL_REGION_LOW = 9
    SPEED_OUTSIDE_CONTROL_REGION_HIGH = 10
    COOL_DOWN = 11
    WATT_CONTROL = 12
    MANUAL_MODE = 13
    PRE_WORKOUT = 14
    POST_WORKOUT = 15
    RESERVED = 16


TrainingStatusMessage = namedtuple(
    "TrainingStatusMessage",
    [
        "param",
        "string",
    ],
)


def parse_training_status(message: bytearray) -> TrainingStatusMessage:
    param = None
    string = None

    param_exists = message[0] & 0b00000001
    string_exists = message[0] & 0b00000010

    if string_exists:
        string = message[2].decode("utf-8")

    if param_exists:
        ts_byte = message[1]
        if ts_byte == 0x00:
            param = TrainingStatus.OTHER
        elif ts_byte == 0x01:
            param = TrainingStatus.IDLE
        elif ts_byte == 0x02:
            param = TrainingStatus.WARMING_UP
        elif ts_byte == 0x03:
            param = TrainingStatus.LOW_INTENSITY_INTERVAL
        elif ts_byte == 0x04:
            param = TrainingStatus.HIGH_INTENSITY_INTERVAL
        elif ts_byte == 0x05:
            param = TrainingStatus.RECOVERY_INTERVAL
        elif ts_byte == 0x06:
            param = TrainingStatus.ISOMETRIC
        elif ts_byte == 0x07:
            param = TrainingStatus.HEART_RATE_CONTROL
        elif ts_byte == 0x08:
            param = TrainingStatus.FITNESS_TEST
        elif ts_byte == 0x09:
            param = TrainingStatus.SPEED_OUTSIDE_CONTROL_REGION_LOW
        elif ts_byte == 0x0A:
            param = TrainingStatus.SPEED_OUTSIDE_CONTROL_REGION_HIGH
        elif ts_byte == 0x0B:
            param = TrainingStatus.COOL_DOWN
        elif ts_byte == 0x0C:
            param = TrainingStatus.WATT_CONTROL
        elif ts_byte == 0x0D:
            param = TrainingStatus.MANUAL_MODE
        elif ts_byte == 0x0E:
            param = TrainingStatus.PRE_WORKOUT
        elif ts_byte == 0x0F:
            param = TrainingStatus.POST_WORKOUT
        elif ts_byte == 0x10:
            param = TrainingStatus.RESERVED
    return TrainingStatusMessage(param, string)
