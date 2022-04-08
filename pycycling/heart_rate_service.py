from collections import namedtuple

heart_rate_measurement_characteristic_id = '00002a37-0000-1000-8000-00805f9b34fb'

HeartRateMeasurement = namedtuple('HeartRateMeasurement', ['sensor_contact', 'bpm', 'rr_interval', 'energy_expended'])


def _parse_hr_measurement(data):
    flags = data[0]

    is_uint16_measurement_mask = 0x01
    is_contact_detected_mask = 0x06
    is_energy_expended_present_mask = 0x08
    is_rr_interval_present_mask = 0x10

    sensor_contact = None
    bpm = None
    rr_interval = []
    energy_expended = None

    measurement_byte_offset = 1
    sensor_contact = bool(flags & is_contact_detected_mask)

    if flags & is_uint16_measurement_mask:
        bpm = int.from_bytes(data[measurement_byte_offset:measurement_byte_offset + 2], 'little')
        measurement_byte_offset += 2
    else:
        bpm = data[measurement_byte_offset]
        measurement_byte_offset += 1

    if flags & is_energy_expended_present_mask:
        energy_expended = int.from_bytes(data[measurement_byte_offset:measurement_byte_offset + 2], 'little')
        measurement_byte_offset += 2

    if flags & is_rr_interval_present_mask:
        while len(data[measurement_byte_offset:]) >= 2:
            rr_interval.append(int.from_bytes(data[measurement_byte_offset:measurement_byte_offset + 2], 'little'))
            measurement_byte_offset += 2

    return HeartRateMeasurement(sensor_contact=sensor_contact,
                                bpm=bpm,
                                rr_interval=rr_interval,
                                energy_expended=energy_expended)


class HeartRateService:
    def __init__(self, client):
        self._client = client
        self._hr_measurement_callback = None

    async def enable_hr_measurement_notifications(self):
        await self._client.start_notify(heart_rate_measurement_characteristic_id,
                                        self._hr_measurement_notification_handler)

    async def disable_hr_measurement_notifications(self):
        await self._client.stop_notify(heart_rate_measurement_characteristic_id)

    def set_hr_measurement_handler(self, callback):
        self._hr_measurement_callback = callback

    def _hr_measurement_notification_handler(self, sender, data):  # pylint: disable=unused-argument
        if self._hr_measurement_callback is not None:
            self._hr_measurement_callback(_parse_hr_measurement(data))
