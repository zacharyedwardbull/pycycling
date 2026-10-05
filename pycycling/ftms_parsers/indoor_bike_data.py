from collections import namedtuple

IndoorBikeData = namedtuple(
    "IndoorBikeData",
    [
        "instant_speed", # km/h
        "average_speed", # km/h
        "instant_cadence", # rpm
        "average_cadence", # rpm
        "total_distance", # m
        "resistance_level", # unitless
        "instant_power", # W
        "average_power", # W
        "total_energy", # kcal
        "energy_per_hour", # kcal/h
        "energy_per_minute", # kcal/min
        "heart_rate", # bpm
        "metabolic_equivalent", # unitless; metas
        "elapsed_time", # s
        "remaining_time", # s
    ]
)
def parse_indoor_bike_data(message) -> IndoorBikeData:
    """Decode a notification, raising ValueError if any advertised field is truncated."""
    if len(message) < 2:
        raise ValueError("Indoor Bike Data requires a two-byte flags field")

    # int.from_bytes accepts short (even empty) slices. Validate the complete
    # advertised layout before parsing so missing bytes cannot become readings.
    # Bit 0 is More Data: unlike the other bits, zero means the field is present.
    # Bit 5 retains this parser's existing signed16 resistance layout; this does
    # not add uint8 resistance support or infer a format from the packet length.
    present = int.from_bytes(message[:2], "little") ^ 1
    field_sizes = (2, 2, 2, 2, 3, 2, 2, 2, 5, 1, 1, 2, 2)
    required_length = 2 + sum(
        size for bit, size in enumerate(field_sizes) if present & (1 << bit)
    )
    if len(message) < required_length:
        raise ValueError(
            "Truncated Indoor Bike Data: expected at least {} bytes, got {}".format(
                required_length, len(message)
            )
        )

    flag_more_data = bool(message[0] & 0b00000001)
    flag_average_speed = bool(message[0] & 0b00000010)
    # ANOMALY: In the Bluetooth SIG spec, instantaneous_cadence is reversed (0
    # means present, 1 means not present). The Huawei docs do not mention this
    # reversal. In practice, the Huawei docs seem correct. There is no
    # reversal.
    flag_instantaneous_cadence = bool(message[0] & 0b00000100)
    flag_average_cadence = bool(message[0] & 0b00001000)
    flag_total_distance = bool(message[0] & 0b00010000)
    flag_resistance_level = bool(message[0] & 0b00100000)
    flag_instantaneous_power = bool(message[0] & 0b01000000)
    flag_average_power = bool(message[0] & 0b10000000)
    flag_expended_energy = bool(message[1] & 0b00000001)
    flag_heart_rate = bool(message[1] & 0b00000010)
    flag_metabolic_equivalent = bool(message[1] & 0b00000100)
    flag_elapsed_time = bool(message[1] & 0b00001000)
    flag_remaining_time = bool(message[1] & 0b00010000)

    instant_speed = None
    average_speed = None
    instant_cadence = None
    average_cadence = None
    total_distance = None
    resistance_level = None
    instant_power = None
    average_power = None
    total_energy = None
    energy_per_hour = None
    energy_per_minute = None
    heart_rate = None
    metabolic_equivalent = None
    elapsed_time = None
    remaining_time = None

    # for each True flag, get the value
    # confusingly, the order of the flags is not the same as the order of the
    # values
    i = 2  # start after the flags
    if flag_more_data == 0:
        instant_speed = int.from_bytes(message[i : i + 2], "little", signed=False)/100
        i += 2
    if flag_average_speed:
        average_speed = int.from_bytes(message[i : i + 2], "little", signed=False)/100
        i += 2
    if flag_instantaneous_cadence:
        instant_cadence = int.from_bytes(message[i : i + 2], "little", signed=False) / 2
        i += 2
    if flag_average_cadence:
        average_cadence = int.from_bytes(message[i : i + 2], "little", signed=False) / 2
        i += 2
    if flag_total_distance:
        total_distance = int.from_bytes(message[i : i + 3], "little", signed=False)
        i += 3
    if flag_resistance_level:
        resistance_level = int.from_bytes(message[i : i + 2], "little", signed=True)
        i += 2
    if flag_instantaneous_power:
        instant_power = int.from_bytes(message[i : i + 2], "little", signed=True)
        i += 2
    if flag_average_power:
        average_power = int.from_bytes(message[i : i + 2], "little", signed=True)
        i += 2
    if flag_expended_energy:
        total_energy = int.from_bytes(message[i : i + 2], "little", signed=False)
        energy_per_hour = int.from_bytes(message[i + 2 : i + 4], "little", signed=False)
        energy_per_minute = int.from_bytes(
            message[i + 4 : i + 5], "little", signed=False
        )
        i += 5
    if flag_heart_rate:
        heart_rate = int.from_bytes(message[i : i + 1], "little", signed=False)
        i += 1
    if flag_metabolic_equivalent:
        metabolic_equivalent = int.from_bytes(
            message[i : i + 1], "little", signed=False
        ) / 10
        i += 1
    if flag_elapsed_time:
        elapsed_time = int.from_bytes(message[i : i + 2], "little", signed=False)
        i += 2
    if flag_remaining_time:
        remaining_time = int.from_bytes(message[i : i + 2], "little", signed=False)
        i += 2

    return IndoorBikeData(
        instant_speed,
        average_speed,
        instant_cadence,
        average_cadence,
        total_distance,
        resistance_level,
        instant_power,
        average_power,
        total_energy,
        energy_per_hour,
        energy_per_minute,
        heart_rate,
        metabolic_equivalent,
        elapsed_time,
        remaining_time,
    )
