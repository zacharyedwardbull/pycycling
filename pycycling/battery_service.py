"""
A module for interacting with Bluetooth devices which support the Battery Service.

Example
=======
This example prints the current battery level to the console. Please see also information on
:ref:`obtaining the Bluetooth address of your device <obtaining_device_address>`.

.. literalinclude:: ../examples/battery_example.py
"""

battery_level_characteristic_id = '00002a19-0000-1000-8000-00805f9b34fb'


def _parse_battery_level(measurement):
    return int.from_bytes(measurement, byteorder='little')


class BatteryService:
    """
    A wrapper around a :obj:`bleak.backends.client.BaseBleakClient` object adding Battery Service specific utility
    methods.

    :param client: A valid :obj:`bleak.backends.client.BaseBleakClient` object
    """

    def __init__(self, client):
        self._client = client

    async def get_battery_level(self):
        """
        Returns current battery level of the Bluetooth device.

        :return: An :obj:`int` representing the current battery level percentage of the Bluetooth device. A value of
            `100` indicates a fully charged battery while `0` a fully discharged battery.
        """
        measurement = await self._client.read_gatt_char(battery_level_characteristic_id)
        return _parse_battery_level(measurement)
