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
        try:
            param = TrainingStatus(ts_byte)
        except ValueError:
            pass
    return TrainingStatusMessage(param, string)
