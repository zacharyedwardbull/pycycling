import sys
import asyncio
import struct
import importlib.resources
import pycycling.data

sterzo_measurement_id = '347b0030-7635-408b-8918-8ff3949ce592'
sterzo_control_point_id = '347b0031-7635-408b-8918-8ff3949ce592'
sterzo_challenge_code_id = '347b0032-7635-408b-8918-8ff3949ce592'


class Sterzo:
    def __init__(self, client):
        self._client = client
        self._steering_measurement_callback = None
        self._latest_challenge = None

    async def enable_steering_measurement_notifications(self):
        await self._client.start_notify(sterzo_challenge_code_id, self._challenge_code_indication_handler)
        await self._client.start_notify(sterzo_measurement_id, self._steering_measurement_notification_handler)
        await self._client.write_gatt_char(sterzo_control_point_id, bytearray([0x03, 0x10]))
        while self._latest_challenge is None:
            await asyncio.sleep(2)
        await self._activate_steering_measurements()

    async def _activate_steering_measurements(self):
        # importlib.resources.path is deprecated since 3.11
        if sys.version_info >= (3, 11):
            challenge_file = importlib.resources.files(pycycling.data).joinpath('sterzo-challenge-codes.dat').open('rb')
        else:  # legacy support < 3.9
            challenge_file = importlib.resources.open_binary(pycycling.data, 'sterzo-challenge-codes.dat') # pylint: disable=deprecated-method

        with challenge_file:
            challenge_file.seek(self._latest_challenge * 2, 1)
            code_1 = int.from_bytes(challenge_file.read(1), 'little')
            code_2 = int.from_bytes(challenge_file.read(1), 'little')

        byte_array = bytearray([0x03, 0x11, code_1, code_2])
        await self._client.write_gatt_char(sterzo_control_point_id, byte_array)
        await asyncio.sleep(1)
        await self._client.write_gatt_char(sterzo_control_point_id, bytearray([0x02, 0x02]))

    async def disable_steering_measurement_notifications(self):
        await self._client.stop_notify(sterzo_measurement_id)

    def set_steering_measurement_callback(self, callback):
        self._steering_measurement_callback = callback

    def _challenge_code_indication_handler(self, sender, data):  # pylint: disable=unused-argument
        self._latest_challenge = int.from_bytes(data[2:4], 'big')

    def _steering_measurement_notification_handler(self, sender, data):  # pylint: disable=unused-argument
        [steering_angle] = struct.unpack('<f', data)
        self._steering_measurement_callback(steering_angle)
