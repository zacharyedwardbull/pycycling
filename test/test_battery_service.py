import unittest

from pycycling.battery_service import _parse_battery_level


class TestBatteryService(unittest.TestCase):
    def test__parse_battery_level(self):
        self.assertEqual(_parse_battery_level(bytearray([0])), 0)
        self.assertEqual(_parse_battery_level(bytearray([42])), 42)
        self.assertEqual(_parse_battery_level(bytearray([100])), 100)


if __name__ == '__main__':
    unittest.main()
