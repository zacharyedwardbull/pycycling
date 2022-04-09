import asyncio
from bleak import BleakClient

from pycycling.heart_rate_service import HeartRateService


async def run(address):
    async with BleakClient(address) as client:
        def my_measurement_handler(data):
            print(data)

        await client.is_connected()
        hr_service = HeartRateService(client)
        hr_service.set_hr_measurement_handler(my_measurement_handler)

        await hr_service.enable_hr_measurement_notifications()
        await asyncio.sleep(30.0)
        await hr_service.disable_hr_measurement_notifications()


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "DEVICE_ADDRESS HERE"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))
