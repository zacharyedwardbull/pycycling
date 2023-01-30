import asyncio
from bleak import BleakClient
from pycycling.fitness_machine_service import FitnessMachineService

async def run(address):
    async with BleakClient(address, timeout=10) as client:
        ftms = FitnessMachineService(client)

        # Print all 'read' characteristics

        supported_resistance_level_range = (
            await ftms.get_supported_resistance_level_range()
        )

        print("Supported resistance level range:")
        print(supported_resistance_level_range)
        print()

        max_resistance = supported_resistance_level_range.maximum_resistance

        supported_power_range = await ftms.get_supported_power_range()

        print("Supported power range:")
        print(supported_power_range)
        print()

        max_power = supported_power_range.maximum_power

        fitness_machine_feature = await ftms.get_fitness_machine_feature()

        print("Fitness machine feature:")
        print(fitness_machine_feature)
        print()

        def print_indoor_bike_data(data):
            print("Received indoor bike data:")
            print(data)
            print()

        # Start receiving and printing 'notify' characteristics
        ftms.set_indoor_bike_data_handler(print_indoor_bike_data)
        await ftms.enable_indoor_bike_data_notify()

        def print_fitness_machine_status(data):
            print("Received fitness machine status:")
            print("\t" + str(data))
            print()

        ftms.set_fitness_machine_status_handler(print_fitness_machine_status)
        await ftms.enable_fitness_machine_status_notify()

        def print_training_status(data):
            print("Received training status:")
            print(data)
            print()

        ftms.set_training_status_handler(print_training_status)
        await ftms.enable_training_status_notify()

        # Write to 'write' characteristics
        # IMPORTANT: Before being able to write, the client (this script) must

        # 1. Start receiving 'indicate' notifications from the control point characteristic
        def print_control_point_response(message):
            print("Received control point response:")
            print(message)
            print()

        ftms.set_control_point_response_handler(print_control_point_response)
        await ftms.enable_control_point_indicate()
        # 2. 'write' a request to control the fitness machine
        await ftms.request_control()
        # 3. (recommended) 'write' a reset command
        await ftms.reset()

        print(
            "Setting target resistance level to 25 percent of maximum resistance level..."
        )
        await ftms.set_target_resistance_level(max_resistance * 0.25)

        await asyncio.sleep(5)

        print(
            "Increasing target resistance level to 50 percent of maximum resistance level..."
        )
        await ftms.set_target_resistance_level(max_resistance * 0.5)

        await asyncio.sleep(5)

        # Reset target resistance level
        print("Resetting target resistance level...")

        await ftms.reset()

        power_level = 4 / 100 * max_power
        print(f"Increasing target power to 4 percent of maximum power ({power_level}W).")
        print("The trainer will automatically adjust resistance based on your leg speed.")
        print("Try pedaling above {power_level}W to feel decreasing resistance, and vice versa.")
        await ftms.set_target_power(power_level)

        await asyncio.sleep(30)

        # Reset
        print("Resetting target power...")
        await ftms.reset()


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "DEVICE_ADDRESS HERE"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address))

    # Unresolved intermittent bug when writing to the control point characteristic:
    # bleak.exc.BleakDBusError: [org.bluez.Error.Failed] Operation failed with ATT error: 0x80 (Unknown code)
    #
    # To work around this, just retry on error, like:
    #
    # import bleak
    # while True:
    #     try:
    #         loop.run_until_complete(run(device_address))
    #     except bleak.exc.BleakDBusError as e:
    #         print("BleakDBusError, retrying...")
    #         print(e)
    #         continue
    #     except KeyboardInterrupt:
    #         break
