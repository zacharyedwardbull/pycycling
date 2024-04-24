import struct

rizer_measurement_id = "347b0030-7635-408b-8918-8ff3949ce592"
rizer_control_point_id = "347b0031-7635-408b-8918-8ff3949ce592"


class Rizer:
    def __init__(self, client):
        self._client = client
        self._steering_measurement_callback = None
        self._latest_challenge = None

    async def enable_steering_measurement_notifications(self):
        await self._client.start_notify(
            rizer_measurement_id, self._steering_measurement_notification_handler
        )

    async def disable_steering_measurement_notifications(self):
        await self._client.stop_notify(rizer_measurement_id)

    def set_steering_measurement_callback(self, callback):
        self._steering_measurement_callback = callback

    def _steering_measurement_notification_handler(
        self, sender, data
    ):  # pylint: disable=unused-argument
        [steering_angle] = struct.unpack("<f", data)
        self._steering_measurement_callback(steering_angle)

    async def set_transmission_rate(self, rate: int):
        """sets the transmission rate of the rizer to 8, 16, or 32 Hz"""
        if rate < 0 or rate > 2:
            raise ValueError(
                "Invalid rate: choose 0, 1, or 2 for 8, 16, or 32 Hz respectively"
            )
        byte_array = b"\x02" + rate.to_bytes(1, "little", signed=False)
        await self._client.write_gatt_char(rizer_control_point_id, byte_array)

    async def set_center(self):
        """sets the zero position of the rizer"""
        await self._client.write_gatt_char(rizer_control_point_id, b"\x01")
