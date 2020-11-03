from collections import namedtuple

cycling_power_measurement_tx_id = '00002a63-0000-1000-8000-00805f9b34fb'

CyclingPowerMeasurement = namedtuple('CyclingPowerMeasurement',
                                     ['instantaneous_power', 'accumulated_energy', 'pedal_power_balance',
                                      'accumulated_torque', 'cumulative_wheel_revs', 'last_wheel_event_time',
                                      'cumulative_crank_revs', 'last_crank_event_time', 'maximum_force_magnitude',
                                      'minimum_force_magnitude', 'maximum_torque_magnitude', 'minimum_torque_magnitude',
                                      'top_dead_spot_angle', 'bottom_dead_spot_angle'])


class CyclingPowerService:
    def __init__(self, client):
        self._client = client
        self._cycling_power_measurement_callback = None

    async def enable_cycling_power_measurement_notifications(self):
        await self._client.start_notify(cycling_power_measurement_tx_id,
                                        self._cycling_power_measurement_notification_handler)

    async def disable_cycling_power_measurement_notifications(self):
        await self._client.stop_notify(cycling_power_measurement_tx_id)

    def set_cycling_power_measurement_handler(self, callback):
        self._cycling_power_measurement_callback = callback

    def _cycling_power_measurement_notification_handler(self, sender, data):
        flags = int.from_bytes(data[0:2], 'little')

        pedal_power_balance_included_flag = 1
        pedal_power_balance_reference_flag = 2
        accumulated_torque_present = 4
        accumulated_torque_source = 8
        wheel_rev_included_flag = 16
        crank_rev_included_flag = 32
        extreme_force_included_flag = 64
        extreme_torque_included_flag = 128
        extreme_angles_included_flag = 256
        top_dead_spot_included_flag = 512
        bottom_dead_spot_included_flag = 1024
        accumulated_energy_included_flag = 2048
        offset_compensation_indicator_flag = 4096

        byte_offset = 2

        instantaneous_power = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')

        pedal_power_balance = None
        accumulated_torque = None
        cumulative_wheel_revs = None
        last_wheel_event_time = None
        cumulative_crank_revs = None
        last_crank_event_time = None
        maximum_force_magnitude = None
        minimum_force_magnitude = None
        maximum_torque_magnitude = None
        minimum_torque_magnitude = None
        top_dead_spot_angle = None
        bottom_dead_spot_angle = None
        accumulated_energy = None

        byte_offset += 2

        if flags & pedal_power_balance_included_flag:
            pedal_power_balance = data[byte_offset]
            byte_offset += 1

        if flags & accumulated_torque_present:
            accumulated_torque = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2

        if flags & wheel_rev_included_flag:
            cumulative_wheel_revs = int.from_bytes(data[0 + byte_offset:4 + byte_offset], 'little')
            byte_offset += 4
            last_wheel_event_time = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2

        if flags & crank_rev_included_flag:
            cumulative_crank_revs = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2
            last_crank_event_time = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2

        if flags & extreme_force_included_flag:
            maximum_force_magnitude = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2
            minimum_force_magnitude = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2

        if flags & extreme_torque_included_flag:
            maximum_torque_magnitude = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2
            minimum_torque_magnitude = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2

        if flags & extreme_angles_included_flag:
            # TODO: Implement extreme angles
            byte_offset += 3

        if flags & top_dead_spot_included_flag:
            top_dead_spot_angle = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2

        if flags & bottom_dead_spot_included_flag:
            bottom_dead_spot_angle = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2

        if flags & accumulated_energy_included_flag:
            accumulated_energy = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')

        if self._cycling_power_measurement_callback is not None:
            self._cycling_power_measurement_callback(
                CyclingPowerMeasurement(instantaneous_power=instantaneous_power, accumulated_energy=accumulated_energy,
                                        pedal_power_balance=pedal_power_balance, accumulated_torque=accumulated_torque,
                                        cumulative_wheel_revs=cumulative_wheel_revs,
                                        last_wheel_event_time=last_wheel_event_time,
                                        cumulative_crank_revs=cumulative_crank_revs,
                                        last_crank_event_time=last_crank_event_time,
                                        maximum_force_magnitude=maximum_force_magnitude,
                                        minimum_force_magnitude=minimum_force_magnitude,
                                        maximum_torque_magnitude=maximum_torque_magnitude,
                                        minimum_torque_magnitude=minimum_torque_magnitude,
                                        top_dead_spot_angle=top_dead_spot_angle,
                                        bottom_dead_spot_angle=bottom_dead_spot_angle))
