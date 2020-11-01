import asyncio
from bleak import BleakClient

from pycycling.tacx_trainer_control import TacxTrainerControl


async def run(address):
    async with BleakClient(address) as client:
        def my_page_handler(data):
            print(data)

        await client.is_connected()
        trainer = TacxTrainerControl(client)
        trainer.set_specific_trainer_data_page_handler(my_page_handler)
        trainer.set_general_fe_data_page_handler(my_page_handler)
        await trainer.enable_fec_notifications()
        await trainer.set_basic_resistance(20)
        await asyncio.sleep(20.0)
        await trainer.set_basic_resistance(40)
        await asyncio.sleep(20.0)
        await trainer.disable_fec_notifications()


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "EAAA3D1F-6760-4D77-961E-8DDAC1CC9AED"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))
