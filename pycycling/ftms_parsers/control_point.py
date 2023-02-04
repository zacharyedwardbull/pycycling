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
    START_OR_RESUME = 0x06
    STOP_OR_PAUSE = 0x07
    RESPONSE_CODE = 0x80


def form_ftms_control_command(opcode: FTMSControlPointOpCode, parameter: int = 0):
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
    elif opcode == FTMSControlPointOpCode.START_OR_RESUME:
        # parameter: 01=stop, 02=pause
        return b"\x06"
    elif opcode == FTMSControlPointOpCode.STOP_OR_PAUSE:
        return b"\x07" + parameter.to_bytes(1, "little", signed=False)
    elif opcode == FTMSControlPointOpCode.RESPONSE_CODE:
        return b"\x80"
    else:
        raise ValueError("Invalid opcode")


ControlPointResponse = namedtuple("ControlPointResponse", ["request_code_enum", "result_code_enum"])


def parse_control_point_response(message: bytearray) -> ControlPointResponse:
    request_code_enum = FTMSControlPointOpCode(message[1])
    result_code_enum = FTMSControlPointResponseResultCode(message[2])
    return ControlPointResponse(request_code_enum, result_code_enum)
