import asyncio
from bleak import BleakClient

from pycycling.cycling_power_service import CyclingPowerService


async def run(address):
    async with BleakClient(address) as client:
        def my_page_handler(data):
            print(data)

        await client.is_connected()
        trainer = CyclingPowerService(client)
        trainer.set_cycling_power_measurement_handler(my_page_handler)
        await trainer.enable_cycling_power_measurement_notifications()
        await asyncio.sleep(30.0)
        await trainer.enable_cycling_power_measurement_notifications()


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = "EAAA3D1F-6760-4D77-961E-8DDAC1CC9AED"  # <--- Change to your device's address here if you are using macOS
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(address))
