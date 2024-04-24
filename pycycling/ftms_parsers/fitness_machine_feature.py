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


TargetSettingFeatures = namedtuple(
    "TargetSettingFeatures",
    [
        "speed_target_setting_supported",
        "inclination_target_setting_supported",
        "resistance_target_setting_supported",
        "power_target_setting_supported",
        "heart_rate_target_setting_supported",
        "targeted_expended_energy_configuration_supported",
        "targeted_step_number_configuration_supported",
        "targeted_stride_number_configuration_supported",
        "targeted_distance_configuration_supported",
        "targeted_training_time_configuration_supported",
        "targeted_time_in_two_heart_rate_zones_configuration_supported",
        "targeted_time_in_three_heart_rate_zones_configuration_supported",
        "targeted_time_in_five_heart_rate_zones_configuration_supported",
        "indoor_bike_simulation_parameters_supported",
        "wheel_circumference_configuration_supported",
        "spin_down_control_supported",
        "targeted_cadence_configuration_supported",
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


def parse_target_setting_features(message: bytearray) -> TargetSettingFeatures:
    speed_target_setting_supported = bool(message[0] & 0b00000001)
    inclination_target_setting_supported = bool(message[0] & 0b00000010)
    resistance_target_setting_supported = bool(message[0] & 0b00000100)
    power_target_setting_supported = bool(message[0] & 0b00001000)
    heart_rate_target_setting_supported = bool(message[0] & 0b00010000)
    targeted_expended_energy_configuration_supported = bool(message[0] & 0b00100000)
    targeted_step_number_configuration_supported = bool(message[0] & 0b01000000)
    targeted_stride_number_configuration_supported = bool(message[0] & 0b10000000)

    targeted_distance_configuration_supported = bool(message[1] & 0b00000001)
    targeted_training_time_configuration_supported = bool(message[1] & 0b00000010)
    targeted_time_in_two_heart_rate_zones_configuration_supported = bool(message[1] & 0b00000100)
    targeted_time_in_three_heart_rate_zones_configuration_supported = bool(message[1] & 0b00001000)
    targeted_time_in_five_heart_rate_zones_configuration_supported = bool(message[1] & 0b00010000)
    indoor_bike_simulation_parameters_supported = bool(message[1] & 0b00100000)
    wheel_circumference_configuration_supported = bool(message[1] & 0b01000000)
    spin_down_control_supported = bool(message[1] & 0b10000000)

    targeted_cadence_configuration_supported = bool(message[2] & 0b00000001)
    return TargetSettingFeatures(
        speed_target_setting_supported,
        inclination_target_setting_supported,
        resistance_target_setting_supported,
        power_target_setting_supported,
        heart_rate_target_setting_supported,
        targeted_expended_energy_configuration_supported,
        targeted_step_number_configuration_supported,
        targeted_stride_number_configuration_supported,
        targeted_distance_configuration_supported,
        targeted_training_time_configuration_supported,
        targeted_time_in_two_heart_rate_zones_configuration_supported,
        targeted_time_in_three_heart_rate_zones_configuration_supported,
        targeted_time_in_five_heart_rate_zones_configuration_supported,
        indoor_bike_simulation_parameters_supported,
        wheel_circumference_configuration_supported,
        spin_down_control_supported,
        targeted_cadence_configuration_supported,
    )

def parse_all_features(message: bytearray):
    return parse_fitness_machine_feature(message[0:4]), parse_target_setting_features(message[4:8])
