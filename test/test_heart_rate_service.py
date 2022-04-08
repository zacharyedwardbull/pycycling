import unittest

from pycycling.heart_rate_service import _parse_hr_measurement, HeartRateMeasurement


class TestHeartRateServiceService(unittest.TestCase):
    def test__parse_csc_measurement(self):
        self.assertEqual(_parse_hr_measurement(
            bytearray([
                0b00000000,  # flags
                0b00101010,  # bpm
            ])),
            HeartRateMeasurement(
                sensor_contact=False,
                bpm=42,
                rr_interval=[],
                energy_expended=None
            )
        )


if __name__ == '__main__':
    unittest.main()
