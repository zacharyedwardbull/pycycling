import asyncio
from bleak import BleakClient

from pycycling.rear_view_radar import RearViewRadarService

async def run(address):
    async with BleakClient(address) as client:
        def my_measurement_handler(data):
            print(data)

        await client.is_connected()
        radar_service = RearViewRadarService(client)
        radar_service.set_radar_measurement_handler(my_measurement_handler)

        await radar_service.enable_radar_measurement_notifications()
        await asyncio.sleep(30.0)
        await radar_service.disable_radar_measurement_notifications()

if __name__ == "__main__":
    import os
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    device_address = "DEVICE_ADDRESS_HERE"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))
