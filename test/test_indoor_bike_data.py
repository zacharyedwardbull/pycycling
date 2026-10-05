import unittest

from pycycling.ftms_parsers.indoor_bike_data import IndoorBikeData, parse_indoor_bike_data


class TestIndoorBikeData(unittest.TestCase):
    # Synthetic Indoor Bike Data (0x2AD2), using this parser's signed16 resistance.
    # Energy is one flag covering three consecutive fields (2 + 2 + 1 bytes).
    all_fields = bytes.fromhex(
        "fe 1f 10 0e ac 0d b5 00 b0 00 56 34 12 f6 ff fa 00 ec ff "
        "7b 00 c8 01 07 96 55 10 0e 08 07"
    )

    def test_all_fields_preserve_units_and_signed_values(self):
        expected = IndoorBikeData(
            36, 35, 90.5, 88, 0x123456, -10, 250, -20,
            123, 456, 7, 150, 8.5, 3600, 1800,
        )
        for container in (bytes, bytearray, memoryview):
            with self.subTest(container=container):
                self.assertEqual(parse_indoor_bike_data(container(self.all_fields)), expected)

    def test_every_truncated_prefix_is_rejected(self):
        for size in range(len(self.all_fields)):
            with self.subTest(size=size):
                with self.assertRaises(ValueError):
                    parse_indoor_bike_data(self.all_fields[:size])

    def test_more_data_does_not_require_speed(self):
        result = parse_indoor_bike_data(bytes.fromhex("45 00 b4 00 fa 00"))
        self.assertIsNone(result.instant_speed)
        self.assertEqual(result.instant_cadence, 90)
        self.assertEqual(result.instant_power, 250)
        self.assertEqual(
            parse_indoor_bike_data(b"\x01\x00"),
            IndoorBikeData(*([None] * 15)),
        )

    def test_all_flag_layout_lengths(self):
        # All 8,192 flag layouts with the parser's existing signed16 resistance.
        widths = (2, 2, 2, 2, 3, 2, 2, 2, 5, 1, 1, 2, 2)
        for flags in range(0x2000):
            payload = flags.to_bytes(2, "little")
            for bit, width in enumerate(widths):
                present = not (flags & 1) if bit == 0 else flags & (1 << bit)
                if present:
                    payload += bytes(width)
            with self.subTest(flags=flags):
                self.assertIsInstance(parse_indoor_bike_data(payload), IndoorBikeData)
                with self.assertRaises(ValueError):
                    parse_indoor_bike_data(payload[:-1])

    def test_resistance_retains_existing_signed16_layout(self):
        self.assertEqual(parse_indoor_bike_data(bytes.fromhex("21 00 fa ff")).resistance_level, -6)
        # The old decoder accidentally accepted the short slice as signed -6;
        # it did not correctly support a uint8 resistance measurement of 250.
        with self.assertRaises(ValueError):
            parse_indoor_bike_data(bytes.fromhex("21 00 fa"))

    def test_trailing_bytes_and_reserved_flags_remain_tolerated(self):
        expected = parse_indoor_bike_data(self.all_fields)
        self.assertEqual(parse_indoor_bike_data(self.all_fields + b"\xaa\xbb"), expected)
        reserved_flags = bytes([self.all_fields[0], self.all_fields[1] | 0xe0])
        self.assertEqual(parse_indoor_bike_data(reserved_flags + self.all_fields[2:]), expected)
