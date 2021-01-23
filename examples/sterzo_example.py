import asyncio
from bleak import BleakClient

from pycycling.sterzo import Sterzo


async def run(address):
    async with BleakClient(address) as client:
        def steering_handler(steering_angle):
            print(steering_angle)

        await client.is_connected()
        sterzo = Sterzo(client)
        sterzo.set_steering_measurement_callback(steering_handler)
        await sterzo.enable_steering_measurement_notifications()
        await asyncio.sleep(60)

if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "36A444C9-2A18-4B6B-B671-E0A8D3DADB1D"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))
