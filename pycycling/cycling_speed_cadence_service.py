from collections import namedtuple

csc_measurement_tx_id = '00002a5b-0000-1000-8000-00805f9b34fb'
csc_feature_tx_id = '00002a5c-0000-1000-8000-00805f9b34fb'

CSCMeasurement = namedtuple('CSCMeasurement',
                            ['cumulative_wheel_revs', 'last_wheel_event_time', 'cumulative_crank_revs',
                             'last_crank_event_time'])

CSCFeature = namedtuple('CSCFeature', ['wheel_rev_supported', 'crank_rev_supported', 'multiple_locations_supported'])


def _parse_csc_feature(measurement):
    value = int.from_bytes(measurement, byteorder='little')
    wheel_rev_supported = bool(value & 0b1)
    crank_rev_supported = bool(value & 0b10)
    multiple_locations_supported = bool(value & 0b100)
    return CSCFeature(wheel_rev_supported=wheel_rev_supported,
                      crank_rev_supported=crank_rev_supported,
                      multiple_locations_supported=multiple_locations_supported)


def _parse_csc_measurement(data):
    flags = data[0]

    wheel_rev_included_flag = 1
    crank_rev_included_flag = 2

    cumulative_wheel_revs = None
    last_wheel_event_time = None
    cumulative_crank_revs = None
    last_crank_event_time = None

    byte_offset = 1
    if flags & wheel_rev_included_flag:
        cumulative_wheel_revs = int.from_bytes(data[0 + byte_offset:4 + byte_offset], 'little')
        last_wheel_event_time = int.from_bytes(data[4 + byte_offset:6 + byte_offset], 'little')
        byte_offset += 6

    if flags & crank_rev_included_flag:
        cumulative_crank_revs = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
        last_crank_event_time = int.from_bytes(data[2 + byte_offset:4 + byte_offset], 'little')

    return CSCMeasurement(cumulative_wheel_revs=cumulative_wheel_revs,
                          last_wheel_event_time=last_wheel_event_time,
                          cumulative_crank_revs=cumulative_crank_revs,
                          last_crank_event_time=last_crank_event_time)


class CyclingSpeedCadenceService:
    def __init__(self, client):
        self._client = client
        self._csc_measurement_callback = None

    async def enable_csc_measurement_notifications(self):
        await self._client.start_notify(csc_measurement_tx_id, self._csc_measurement_notification_handler)

    async def disable_csc_measurement_notifications(self):
        await self._client.stop_notify(csc_measurement_tx_id)

    def set_csc_measurement_handler(self, callback):
        self._csc_measurement_callback = callback

    async def get_csc_feature(self):
        measurement = await self._client.read_gatt_char(csc_feature_tx_id)
        return _parse_csc_feature(measurement)

    def _csc_measurement_notification_handler(self, sender, data):  # pylint: disable=unused-argument
        if self._csc_measurement_callback is not None:
            self._csc_measurement_callback(_parse_csc_measurement(data))
