import unittest

from pycycling.cycling_speed_cadence_service import _parse_csc_feature, _parse_csc_measurement, CSCFeature, \
    CSCMeasurement


class TestCyclingSpeedCadenceService(unittest.TestCase):
    def test__parse_csc_feature(self):
        self.assertEqual(_parse_csc_feature(
            bytearray([
                0b00000111, 0b00000000
            ])),
            CSCFeature(
                wheel_rev_supported=True,
                crank_rev_supported=True,
                multiple_locations_supported=True
            )
        )

        self.assertEqual(_parse_csc_feature(
            bytearray([
                0b00000101, 0b00000000
            ])),
            CSCFeature(
                wheel_rev_supported=True,
                crank_rev_supported=False,
                multiple_locations_supported=True
            )
        )

        self.assertEqual(_parse_csc_feature(
            bytearray([
                0b00000000, 0b00000000
            ])),
            CSCFeature(
                wheel_rev_supported=False,
                crank_rev_supported=False,
                multiple_locations_supported=False
            )
        )

    def test__parse_csc_measurement(self):
        self.assertEqual(_parse_csc_measurement(
            bytearray([
                0b00000011,  # flags
                0b11111111, 0b11111111, 0b11111111, 0b11111111,  # wheel revs
                0b00000011, 0b00111111,  # last wheel event time
                0b11111111, 0b00000111,  # crank revs
                0b11100111, 0b00001111,  # last crank event time
            ])),
            CSCMeasurement(
                cumulative_wheel_revs=4294967295,
                last_wheel_event_time=16131,
                cumulative_crank_revs=2047,
                last_crank_event_time=4071
            )
        )


if __name__ == '__main__':
    unittest.main()
