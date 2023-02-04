from collections import namedtuple

FitnessMachineFeature = namedtuple(
    "FitnessMachineFeature",
    [
        "avg_speed_supported",
        "cadence_supported",
        "total_distance_supported",
        "inclination_supported",
        "elevation_gain_supported",
        "pace_supported",
        "step_count_supported",
        "resistance_level_supported",
        "stride_count_supported",
        "expended_energy_supported",
        "heart_rate_measurement_supported",
        "metabolic_equivalent_supported",
        "elapsed_time_supported",
        "remaining_time_supported",
        "power_measurement_supported",
        "force_on_belt_and_power_output_supported",
        "user_data_retention_supported",
    ],
)


def parse_fitness_machine_feature(message: bytearray) -> FitnessMachineFeature:
    """Bit flags are set across two message"""
    avg_speed_supported = bool(message[0] & 0b00000001)
    cadence_supported = bool(message[0] & 0b00000010)
    total_distance_supported = bool(message[0] & 0b00000100)
    inclination_supported = bool(message[0] & 0b00001000)
    elevation_gain_supported = bool(message[0] & 0b00010000)
    pace_supported = bool(message[0] & 0b00100000)
    step_count_supported = bool(message[0] & 0b01000000)
    resistance_level_supported = bool(message[0] & 0b10000000)
    stride_count_supported = bool(message[1] & 0b00000001)
    expended_energy_supported = bool(message[1] & 0b00000010)
    heart_rate_measurement_supported = bool(message[1] & 0b00000100)
    metabolic_equivalent_supported = bool(message[1] & 0b00001000)
    elapsed_time_supported = bool(message[1] & 0b00010000)
    remaining_time_supported = bool(message[1] & 0b00100000)
    power_measurement_supported = bool(message[1] & 0b01000000)
    force_on_belt_and_power_output_supported = bool(message[1] & 0b10000000)
    user_data_retention_supported = bool(message[2] & 0b00000001)
    return FitnessMachineFeature(
        avg_speed_supported,
        cadence_supported,
        total_distance_supported,
        inclination_supported,
        elevation_gain_supported,
        pace_supported,
        step_count_supported,
        resistance_level_supported,
        stride_count_supported,
        expended_energy_supported,
        heart_rate_measurement_supported,
        metabolic_equivalent_supported,
        elapsed_time_supported,
        remaining_time_supported,
        power_measurement_supported,
        force_on_belt_and_power_output_supported,
        user_data_retention_supported,
    )
