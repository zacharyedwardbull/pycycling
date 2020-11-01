import asyncio
from bleak import BleakClient

from pycycling.cycling_speed_cadence_service import CyclingSpeedCadenceService


async def run(address):
    async with BleakClient(address) as client:
        def my_page_handler(data):
            print(data)

        await client.is_connected()
        trainer = CyclingSpeedCadenceService(client)
        trainer.set_csc_measurement_handler(my_page_handler)
        await trainer.enable_csc_measurement_notifications()
        await asyncio.sleep(30.0)
        await trainer.disable_csc_measurement_notifications()


if __name__ == "__main__":
    device_address = "EAAA3D1F-6760-4D77-961E-8DDAC1CC9AED"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))
