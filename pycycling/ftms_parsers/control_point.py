from enum import Enum
from collections import namedtuple


class FTMSControlPointResponseResultCode(Enum):
    SUCCESS = 0x01
    NOT_SUPPORTED = 0x02
    INCORRECT_PARAMETER = 0x03
    OPERATION_FAILED = 0x04
    CONTROL_NOT_PERMITTED = 0x05

class FTMSControlPointOpCode(Enum):
    REQUEST_CONTROL = 0x00
    RESET = 0x01
    SET_TARGET_SPEED = 0x02
    SET_TARGET_INCLINE = 0x03
    SET_TARGET_RESISTANCE_LEVEL = 0x04
    SET_TARGET_POWER = 0x05
    SET_TARGET_HEART_RATE = 0x06
    START_OR_RESUME = 0x07
    STOP_OR_PAUSE = 0x08
    SET_TARGETED_EXPENDED_ENERGY = 0x09
    SET_TARGETED_NUMBER_OF_STEPS = 0x0A
    SET_TARGETED_NUMBER_OF_STRIDES = 0x0B
    SET_TARGETED_DISTANCE = 0x0C
    SET_TARGETED_TRAINING_TIME = 0x0D
    SET_TARGETED_TIME_IN_TWO_HEART_RATE_ZONES = 0x0E
    SET_TARGETED_TIME_IN_THREE_HEART_RATE_ZONES = 0x0F
    SET_TARGETED_TIME_IN_FIVE_HEART_RATE_ZONES = 0x10
    SET_INDOOR_BIKE_SIMULATION_PARAMETERS = 0x11
    SET_WHEEL_CIRCUMFERENCE = 0x12
    SET_SPIN_DOWN_CONTROL = 0x13
    SET_TARGETED_CADENCE = 0x14
    RESPONSE_CODE = 0x80

def form_ftms_control_command(opcode: FTMSControlPointOpCode, parameter: int = 0):
    """
    Form a FTMS control command message
    :param opcode: FTMSControlPointOpCode
    :param parameter: scalar or list of scalar
    :return: bytearray
    """
    parameter = parameter if isinstance(parameter, list) else (int)(parameter)
    if opcode == FTMSControlPointOpCode.REQUEST_CONTROL:
        return b"\x00"
    elif opcode == FTMSControlPointOpCode.RESET:
        return b"\x01"
    elif opcode == FTMSControlPointOpCode.SET_TARGET_SPEED:
        # parameter: uint16, 0.01km/h
        return b"\x02" + parameter.to_bytes(2, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_TARGET_INCLINE:
        # parameter: sint16, 0.1%
        return b"\x03" + parameter.to_bytes(2, "little", signed=True)
    elif opcode == FTMSControlPointOpCode.SET_TARGET_RESISTANCE_LEVEL:
        # parameter: uint8, 0.1 unitless
        return b"\x04" + parameter.to_bytes(1, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_TARGET_POWER:
        # parameter: sint16, 1W
        return b"\x05" + parameter.to_bytes(2, "little", signed=True)
    elif opcode == FTMSControlPointOpCode.SET_TARGET_HEART_RATE:
        # parameter: uint8, 1bpm
        return b"\x06" + parameter.to_bytes(1, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.START_OR_RESUME:
        return b"\x07"
    elif opcode == FTMSControlPointOpCode.STOP_OR_PAUSE:
        # parameter: 01=stop, 02=pause
        return b"\x08" + parameter.to_bytes(1, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.RESPONSE_CODE:
        return b"\x80"
    elif opcode == FTMSControlPointOpCode.SET_TARGETED_EXPENDED_ENERGY:
        # parameter: uint16, 1calories
        return b"\x09" + parameter.to_bytes(2, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_TARGETED_NUMBER_OF_STEPS:
        # parameter: uint16, 1
        return b"\x0A" + parameter.to_bytes(2, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_TARGETED_NUMBER_OF_STRIDES:
        # parameter: uint16, 1
        return b"\x0B" + parameter.to_bytes(2, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_TARGETED_DISTANCE:
        # parameter: uint24, 1m
        return b"\x0C" + parameter.to_bytes(3, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_TARGETED_TRAINING_TIME:
        # parameter: uint16, 1s
        return b"\x0D" + parameter.to_bytes(2, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_TARGETED_TIME_IN_TWO_HEART_RATE_ZONES:
        # parameter: list of 2 uint16, 1s
        return b"\x0E" + parameter[0].to_bytes(2, "little", signed=False) \
                + parameter[1].to_bytes(2, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_TARGETED_TIME_IN_THREE_HEART_RATE_ZONES:
        # parameter: list of 3 uint16, 1s
        return  b"\x0F" + parameter[0].to_bytes(2, "little", signed=False) \
                + parameter[1].to_bytes(2, "little", signed=False) \
                + parameter[2].to_bytes(2, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_TARGETED_TIME_IN_FIVE_HEART_RATE_ZONES:
        # parameter: list of 5 uint16, 1s
        return b"\x10" + parameter[0].to_bytes(2, "little", signed=False) \
                + parameter[1].to_bytes(2, "little", signed=False) \
                + parameter[2].to_bytes(2, "little", signed=False) \
                + parameter[3].to_bytes(2, "little", signed=False) \
                + parameter[4].to_bytes(2, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_INDOOR_BIKE_SIMULATION_PARAMETERS:
        # parameter: list of int16 0.001mps, int16 0.01%, uint8 0.0001, uint8 0.01kg/m
        return b"\x11" + parameter[0].to_bytes(2, "little", signed=True) \
                + parameter[1].to_bytes(2, "little", signed=True) \
                + parameter[2].to_bytes(1, "little", signed=False) \
                + parameter[3].to_bytes(1, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_WHEEL_CIRCUMFERENCE:
        # parameter: uint16, 0.1mm
        return b"\x12" + parameter.to_bytes(2, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_SPIN_DOWN_CONTROL:
        # parameter: 01=start, 02=ignore
        return b"\x13" + parameter.to_bytes(1, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.SET_TARGETED_CADENCE:
        # parameter: uint16, 1rpm
        return b"\x14" + parameter.to_bytes(1, "little", signed=False)
    else:
        raise ValueError("Invalid opcode")


ControlPointResponse = namedtuple("ControlPointResponse", ["request_code_enum", "result_code_enum"])


def parse_control_point_response(message: bytearray) -> ControlPointResponse:
    request_code_enum = FTMSControlPointOpCode(message[1])
    result_code_enum = FTMSControlPointResponseResultCode(message[2])
    return ControlPointResponse(request_code_enum, result_code_enum)
