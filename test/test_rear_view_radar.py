import unittest

from pycycling.rear_view_radar import _parse_radar_measurement, RadarMeasurement


class TestRearViewRadar(unittest.TestCase):
    def test__parse_radar_measurement(self):
        self.assertEqual(_parse_radar_measurement(
            bytearray(b'\x12\x83\x03\x1f\x8f\x1c-\x97=G')
            ),
                [
                RadarMeasurement(
                    threat_id = 131, # byte 1+3i
                    distance = 3, # byte 2+3i: in meters
                    speed = 31, # byte 3+3i: in km/h
                    ),
                RadarMeasurement( # different car
                    threat_id = 143, # as identified by different threat_id
                    distance = 28,
                    speed = 45,
                    ),
                RadarMeasurement( # third car
                    threat_id = 151,
                    distance = 61,
                    speed = 71
                    ),
                ]
            )

if __name__ == '__main__':
    unittest.main()
