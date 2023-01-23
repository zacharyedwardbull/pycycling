def parse_indoor_bike_data(message) -> dict:
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

    # for each True flag, get the value
    # confusingly, the order of the flags is not the same as the order of the
    # values
    i = 2  # start after the flags
    values = {}
    if flag_more_data == 0:
        instant_speed = int.from_bytes(message[i : i + 2], "little", signed=False)
        values["instant_speed"] = (instant_speed / 100, "km/h")
        i += 2
    if flag_average_speed:
        average_speed = int.from_bytes(message[i : i + 2], "little", signed=False)
        values["average_speed"] = (average_speed / 100, "km/h")
        i += 2
    if flag_instantaneous_cadence:
        instant_cadence = int.from_bytes(message[i : i + 2], "little", signed=False)
        values["instant_cadence"] = (instant_cadence / 2, "rpm")
        i += 2
    if flag_average_cadence:
        average_cadence = int.from_bytes(message[i : i + 2], "little", signed=False)
        values["average_cadence"] = (average_cadence / 2, "rpm")
        i += 2
    if flag_total_distance:
        total_distance = int.from_bytes(message[i : i + 3], "little", signed=False)
        values["total_distance"] = (total_distance, "m")
        i += 3
    if flag_resistance_level:
        resistance_level = int.from_bytes(message[i : i + 2], "little", signed=True)
        values["resistance_level"] = (resistance_level, "unitless")
        i += 2
    if flag_instantaneous_power:
        instant_power = int.from_bytes(message[i : i + 2], "little", signed=True)
        values["instant_power"] = (instant_power, "W")
        i += 2
    if flag_average_power:
        average_power = int.from_bytes(message[i : i + 2], "little", signed=True)
        values["average_power"] = (average_power, "W")
        i += 2
    if flag_expended_energy:
        total_energy = int.from_bytes(message[i : i + 2], "little", signed=False)
        values["total_energy"] = (total_energy, "kcal")
        energy_per_hour = int.from_bytes(message[i + 2 : i + 4], "little", signed=False)
        values["energy_per_hour"] = (energy_per_hour, "kcal/h")
        energy_per_minute = int.from_bytes(
            message[i + 4 : i + 5], "little", signed=False
        )
        values["energy_per_minute"] = (energy_per_minute, "kcal/min")
        i += 5
    if flag_heart_rate:
        heart_rate = int.from_bytes(message[i : i + 1], "little", signed=False)
        values["heart_rate"] = (heart_rate, "bpm")
        i += 1
    if flag_metabolic_equivalent:
        metabolic_equivalent = int.from_bytes(
            message[i : i + 1], "little", signed=False
        )
        values["metabolic_equivalent"] = (metabolic_equivalent / 10, "metas")
        i += 1
    if flag_elapsed_time:
        elapsed_time = int.from_bytes(message[i : i + 2], "little", signed=False)
        values["elapsed_time"] = (elapsed_time, "s")
        i += 2
    if flag_remaining_time:
        remaining_time = int.from_bytes(message[i : i + 2], "little", signed=False)
        values["remaining_time"] = (remaining_time, "s")
        i += 2

    return values
