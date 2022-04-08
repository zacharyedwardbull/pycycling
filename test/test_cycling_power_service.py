import unittest

from pycycling.cycling_power_service import _parse_sensor_location, _parse_cycling_power_feature, \
    _parse_cycling_power_measurement, SensorLocation, CyclingPowerFeature, SensorMeasurementContext, \
    DistributeSystemSupport, CyclingPowerMeasurement


class TestCyclingPowerService(unittest.TestCase):
    def test__parse_sensor_location(self):
        self.assertEqual(_parse_sensor_location(bytearray([0])), SensorLocation.other)
        self.assertEqual(_parse_sensor_location(bytearray([3])), SensorLocation.hip)
        self.assertEqual(_parse_sensor_location(bytearray([5])), SensorLocation.left_crank)
        self.assertEqual(_parse_sensor_location(bytearray([17])), None)

    def test__parse_cycling_power_feature(self):
        # device which supports everything
        self.assertEqual(_parse_cycling_power_feature(
            bytearray([
                0b11111111, 0b11111111, 0b11111111, 0b00000000
            ])),
            CyclingPowerFeature(
                pedal_power_balance_supported=True,
                accumulated_torque_supported=True,
                wheel_rev_supported=True,
                crank_rev_supported=True,
                extreme_magnitudes_supported=True,
                dead_spot_angles_supported=True,
                accumulated_energy_supported=True,
                offset_compensation_supported=True,
                cycling_power_measurement_content_masking_supported=True,
                multiple_locations_supported=True,
                crank_length_adjustment_supported=True,
                chain_length_adjustment_supported=True,
                chain_weight_adjustment_supported=True,
                span_length_adjustment_supported=True,
                sensor_measurement_context=SensorMeasurementContext.torque_based,
                instantaneous_measurement_direction_supported=True,
                factory_calibration_date_supported=True,
                enhanced_offset_compensation_supported=True,
                distribute_system_support=DistributeSystemSupport.unspecified
            )
        )
        # device which supports nothing
        self.assertEqual(_parse_cycling_power_feature(
            bytearray([
                0b00000000, 0b00000000, 0b00000000, 0b00000000
            ])),
            CyclingPowerFeature(
                pedal_power_balance_supported=False,
                accumulated_torque_supported=False,
                wheel_rev_supported=False,
                crank_rev_supported=False,
                extreme_magnitudes_supported=False,
                dead_spot_angles_supported=False,
                accumulated_energy_supported=False,
                offset_compensation_supported=False,
                cycling_power_measurement_content_masking_supported=False,
                multiple_locations_supported=False,
                crank_length_adjustment_supported=False,
                chain_length_adjustment_supported=False,
                chain_weight_adjustment_supported=False,
                span_length_adjustment_supported=False,
                sensor_measurement_context=SensorMeasurementContext.force_based,
                instantaneous_measurement_direction_supported=False,
                factory_calibration_date_supported=False,
                enhanced_offset_compensation_supported=False,
                distribute_system_support=DistributeSystemSupport.unspecified
            )
        )

    def test__parse_cycling_power_measurement(self):
        # Simple case, just power and no bells and whistles
        self.assertEqual(_parse_cycling_power_measurement(
            bytearray([
                0b00000000, 0b00000000,  # flags
                0b11010010, 0b00000100,  # power data
            ])),
            CyclingPowerMeasurement(
                instantaneous_power=1234,
                accumulated_energy=None,
                pedal_power_balance=None,
                accumulated_torque=None,
                cumulative_wheel_revs=None,
                last_wheel_event_time=None,
                cumulative_crank_revs=None,
                last_crank_event_time=None,
                maximum_force_magnitude=None,
                minimum_force_magnitude=None,
                maximum_torque_magnitude=None,
                minimum_torque_magnitude=None,
                top_dead_spot_angle=None,
                bottom_dead_spot_angle=None
            )
        )

        # Include crank data
        self.assertEqual(_parse_cycling_power_measurement(
            bytearray([
                0b00110000, 0b00000000,  # flags
                0b11010010, 0b00000100,  # power data
                0b11111111, 0b11111111, 0b11111111, 0b11111111,  # wheel revs
                0b00000011, 0b00111111,  # last wheel event time
                0b11111111, 0b00000111,  # crank revs
                0b11100111, 0b00001111,  # last crank event time
            ])),
            CyclingPowerMeasurement(
                instantaneous_power=1234,
                accumulated_energy=None,
                pedal_power_balance=None,
                accumulated_torque=None,
                cumulative_wheel_revs=4294967295,
                last_wheel_event_time=16131,
                cumulative_crank_revs=2047,
                last_crank_event_time=4071,
                maximum_force_magnitude=None,
                minimum_force_magnitude=None,
                maximum_torque_magnitude=None,
                minimum_torque_magnitude=None,
                top_dead_spot_angle=None,
                bottom_dead_spot_angle=None
            )
        )


if __name__ == '__main__':
    unittest.main()
