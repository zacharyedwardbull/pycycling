battery_level_characteristic_id = '00002a19-0000-1000-8000-00805f9b34fb'


def _parse_battery_level(measurement):
    return int.from_bytes(measurement, byteorder='little')


class BatteryService:
    def __init__(self, client):
        self._client = client

    async def get_battery_level(self):
        measurement = await self._client.read_gatt_char(battery_level_characteristic_id)
        return _parse_battery_level(measurement)
