import asyncio
from bleak import BleakClient

from pycycling.rizer import Rizer

""" make sure the rizer is connected to a fitness machine otherwise the steering angle will not be transmitted """


async def run(address):
    async with BleakClient(address) as client:
        def steering_handler(steering_angle):
            print(steering_angle)

        await client.is_connected()
        rizer = Rizer(client)
        rizer.set_steering_measurement_callback(steering_handler)
        await rizer.enable_steering_measurement_notifications()
        await rizer.set_transmission_rate(0) # 8 Hz
        await asyncio.sleep(4)
        await rizer.set_transmission_rate(1) # 16 Hz
        await asyncio.sleep(4)
        await rizer.set_transmission_rate(2) # 32 Hz
        await asyncio.sleep(4)
        # recalibrate the rizer
        #await rizer.set_center()

if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "YOUR RIZER ADDRESS HERE"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))
