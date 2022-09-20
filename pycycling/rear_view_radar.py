""" A module for interacting with Bluetooth LE devices which support the Radar (RDR) service

Jason Sohn 2022

This service is tested on Garmin Varia RVR315.
Other models which are expected to support RDR service are:

* Garmin RTR515, RTR516 (German market version), and RCT715
* Bryton Gardia R300
* Magene L508

Example
=======
This example prints radar information broadcast from the Bluetooth device to the console. Please see also
information on :ref:`obtaining the Bluetooth address of your device <obtaining_device_address>`.

.. literalinclude:: ../examples/rear_view_radar_example.py
"""

from collections import namedtuple

radar_characteristic_id = '6a4e3203-667b-11e3-949a-0800200c9a66'

RadarMeasurement = namedtuple('RadarMeasurement', [
    'threat_id',
    'speed',
    'distance',
])

def _parse_radar_measurement(data: bytearray) -> RadarMeasurement:
    """
    Characteristic payload in bytes: 1+3i where i is number of threats (cars)

    byte 0: probably some kind of packet identifier (can be used in case of multiple packets)
    byte 1: threat identifier
    byte 2 (5, 8, ...): distance to threat in meters
    byte 3 (6, 9, ...): speed of threat in km/h

    See source for this reverse-engineering in repo README
    """
    radar_measurements = []
    try:
        for i in range(1, len(data), 3):
            threat_id = int(data[i])
            distance = int(data[i+1])
            speed = int(data[i+2])
            radar_measurements.append(RadarMeasurement(threat_id, speed, distance))
    except IndexError:
        print('pycycling:rear_view_radar.py IndexError: probably starting up and not all data is available yet')
        return None
    return radar_measurements

class RearViewRadarService:
    def __init__(self, client):
        self._client = client
        self._radar_measurement_callback = None

    async def enable_radar_measurement_notifications(self):
        await self._client.start_notify(radar_characteristic_id, self._radar_measurement_notification_handler)

    async def disable_radar_measurement_notifications(self):
        await self._client.stop_notify(radar_characteristic_id)

    def set_radar_measurement_handler(self, callback):
        self._radar_measurement_callback = callback

    def _radar_measurement_notification_handler(self, sender, data): # pylint: disable=unused-argument
        if self._radar_measurement_callback is not None:
            self._radar_measurement_callback(_parse_radar_measurement(data))
