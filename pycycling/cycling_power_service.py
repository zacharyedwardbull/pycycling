from collections import namedtuple
from enum import Enum

cycling_power_measurement_tx_id = '00002a63-0000-1000-8000-00805f9b34fb'
cycling_power_vector_tx_id = '00002a64-0000-1000-8000-00805f9b34fb'
cycling_power_feature_tx_id = '00002a65-0000-1000-8000-00805f9b34fb'
sensor_location_tx_id = '00002a5d-0000-1000-8000-00805f9b34fb'

SensorMeasurementContext = Enum('SensorMeasurementContext', 'force_based torque_based')

DistributeSystemSupport = Enum('DistributeSystemSupport',
                               'unspecified no_distributed_system_support distributed_system_support rfu')

SensorLocation = Enum('SensorLocation',
                      'other top_of_shoe in_shoe hip front_wheel left_crank right_crank left_pedal right_pedal '
                      'front_hub rear_dropout chainstay rear_wheel rear_hub chest spider chain_ring')

InstantaneousMeasurementDirection = Enum('InstantaneousMeasurementDirection',
                                         'unknown tangential_component radial_component lateral_component')

CyclingPowerMeasurement = namedtuple('CyclingPowerMeasurement',
                                     ['instantaneous_power', 'accumulated_energy', 'pedal_power_balance',
                                      'accumulated_torque', 'cumulative_wheel_revs', 'last_wheel_event_time',
                                      'cumulative_crank_revs', 'last_crank_event_time', 'maximum_force_magnitude',
                                      'minimum_force_magnitude', 'maximum_torque_magnitude', 'minimum_torque_magnitude',
                                      'top_dead_spot_angle', 'bottom_dead_spot_angle'])

CyclingPowerFeature = namedtuple('CyclingPowerFeature',
                                 ['pedal_power_balance_supported', 'accumulated_torque_supported',
                                  'wheel_rev_supported', 'crank_rev_supported', 'extreme_magnitudes_supported',
                                  'dead_spot_angles_supported', 'accumulated_energy_supported',
                                  'offset_compensation_supported',
                                  'cycling_power_measurement_content_masking_supported', 'multiple_locations_supported',
                                  'crank_length_adjustment_supported', 'chain_length_adjustment_supported',
                                  'chain_weight_adjustment_supported', 'span_length_adjustment_supported',
                                  'sensor_measurement_context', 'instantaneous_measurement_direction_supported',
                                  'factory_calibration_date_supported', 'enhanced_offset_compensation_supported',
                                  'distribute_system_support'])

CyclingPowerVector = namedtuple('CyclingPowerVector',
                                ['instantaneous_measurement_direction', 'cumulative_crank_revs',
                                 'last_crank_event_time', 'first_crank_measurement_angle',
                                 'instantaneous_force_magnitudes', 'instantaneous_torque_magnitudes'])


class CyclingPowerService:
    def __init__(self, client):
        self._client = client
        self._cycling_power_measurement_callback = None
        self._cycling_power_vector_callback = None

    async def enable_cycling_power_measurement_notifications(self):
        await self._client.start_notify(cycling_power_measurement_tx_id,
                                        self._cycling_power_measurement_notification_handler)

    async def disable_cycling_power_measurement_notifications(self):
        await self._client.stop_notify(cycling_power_measurement_tx_id)

    def set_cycling_power_measurement_handler(self, callback):
        self._cycling_power_measurement_callback = callback

    async def enable_cycling_power_vector_notifications(self):
        await self._client.start_notify(cycling_power_vector_tx_id,
                                        self._cycling_power_vector_notification_handler)

    async def disable_cycling_power_vector_notifications(self):
        await self._client.stop_notify(cycling_power_vector_tx_id)

    def set_cycling_power_vector_handler(self, callback):
        self._cycling_power_vector_callback = callback

    async def get_sensor_location(self):
        measurement = await self._client.read_gatt_char(sensor_location_tx_id)
        value = int.from_bytes(measurement, 'little')

        if value == 0:
            return SensorLocation.other
        elif value == 1:
            return SensorLocation.top_of_shoe
        elif value == 2:
            return SensorLocation.in_shoe
        elif value == 3:
            return SensorLocation.hip
        elif value == 4:
            return SensorLocation.front_wheel
        elif value == 5:
            return SensorLocation.left_crank
        elif value == 6:
            return SensorLocation.right_crank
        elif value == 7:
            return SensorLocation.left_pedal
        elif value == 8:
            return SensorLocation.right_pedal
        elif value == 9:
            return SensorLocation.front_hub
        elif value == 10:
            return SensorLocation.rear_dropout
        elif value == 11:
            return SensorLocation.chainstay
        elif value == 12:
            return SensorLocation.rear_wheel
        elif value == 13:
            return SensorLocation.rear_hub
        elif value == 14:
            return SensorLocation.chest
        elif value == 15:
            return SensorLocation.spider
        elif value == 16:
            return SensorLocation.chain_ring

        return None

    async def get_cycling_power_feature(self):
        measurement = await self._client.read_gatt_char(cycling_power_feature_tx_id)
        value = int.from_bytes(measurement, byteorder='little')
        pedal_power_balance_supported = bool(value & 0b1)
        accumulated_torque_supported = bool(value & 0b10)
        wheel_rev_supported = bool(value & 0b100)
        crank_rev_supported = bool(value & 0b1000)
        extreme_magnitudes_supported = bool(value & 0b10000)
        dead_spot_angles_supported = bool(value & 0b100000)
        accumulated_energy_supported = bool(value & 0b1000000)
        offset_compensation_supported = bool(value & 0b10000000)
        cycling_power_measurement_content_masking_supported = bool(value & 0b100000000)
        multiple_locations_supported = bool(value & 0b1000000000)
        crank_length_adjustment_supported = bool(value & 0b10000000000)
        chain_length_adjustment_supported = bool(value & 0b100000000000)
        chain_weight_adjustment_supported = bool(value & 0b1000000000000)
        span_length_adjustment_supported = bool(value & 0b10000000000000)

        sensor_measurement_context_value = bool(value & 0b100000000000000)
        sensor_measurement_context = SensorMeasurementContext.force_based

        if sensor_measurement_context_value:
            sensor_measurement_context = SensorMeasurementContext.torque_based

        instantaneous_measurement_direction_supported = bool(value & 0b1000000000000000)
        factory_calibration_date_supported = bool(value & 0b10000000000000000)
        enhanced_offset_compensation_supported = bool(value & 0b100000000000000000)

        distribute_system_support_value = (value & 0b11000000000000000000) >> 20

        distribute_system_support = DistributeSystemSupport.unspecified

        if distribute_system_support_value == 1:
            distribute_system_support = DistributeSystemSupport.no_distributed_system_support
        elif distribute_system_support_value == 2:
            distribute_system_support = DistributeSystemSupport.distributed_system_support
        elif distribute_system_support == 3:
            distribute_system_support = DistributeSystemSupport.rfu

        return CyclingPowerFeature(
            pedal_power_balance_supported=pedal_power_balance_supported,
            accumulated_torque_supported=accumulated_torque_supported,
            wheel_rev_supported=wheel_rev_supported, crank_rev_supported=crank_rev_supported,
            extreme_magnitudes_supported=extreme_magnitudes_supported,
            dead_spot_angles_supported=dead_spot_angles_supported,
            accumulated_energy_supported=accumulated_energy_supported,
            offset_compensation_supported=offset_compensation_supported,
            cycling_power_measurement_content_masking_supported=cycling_power_measurement_content_masking_supported,
            multiple_locations_supported=multiple_locations_supported,
            crank_length_adjustment_supported=crank_length_adjustment_supported,
            chain_length_adjustment_supported=chain_length_adjustment_supported,
            chain_weight_adjustment_supported=chain_weight_adjustment_supported,
            span_length_adjustment_supported=span_length_adjustment_supported,
            sensor_measurement_context=sensor_measurement_context,
            instantaneous_measurement_direction_supported=instantaneous_measurement_direction_supported,
            factory_calibration_date_supported=factory_calibration_date_supported,
            enhanced_offset_compensation_supported=enhanced_offset_compensation_supported,
            distribute_system_support=distribute_system_support
        )

    def _cycling_power_measurement_notification_handler(self, sender, data):
        flags = int.from_bytes(data[0:2], 'little')

        pedal_power_balance_included_flag = 0b1
        pedal_power_balance_reference_flag = 0b10
        accumulated_torque_present = 0b100
        accumulated_torque_source = 0b1000
        wheel_rev_included_flag = 0b10000
        crank_rev_included_flag = 0b100000
        extreme_force_included_flag = 0b1000000
        extreme_torque_included_flag = 0b10000000
        extreme_angles_included_flag = 0b100000000
        top_dead_spot_included_flag = 0b1000000000
        bottom_dead_spot_included_flag = 0b10000000000
        accumulated_energy_included_flag = 0b100000000000
        offset_compensation_indicator_flag = 0b1000000000000

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

    def _cycling_power_vector_notification_handler(self, sender, data):
        flags = data[0]

        crank_revolutions_present = bool(flags & 0b1)
        first_crank_measurement_angle_present = bool(flags & 0b10)
        instantaneous_force_array_present = bool(flags & 0b100)
        instantaneous_torque_array_present = bool(flags & 0b1000)
        instantaneous_measurement_direction_value = (flags & 0b110000) >> 4

        instantaneous_measurement_direction = InstantaneousMeasurementDirection.unknown

        if instantaneous_measurement_direction_value == 1:
            instantaneous_measurement_direction = InstantaneousMeasurementDirection.tangential_component
        elif instantaneous_measurement_direction_value == 2:
            instantaneous_measurement_direction = InstantaneousMeasurementDirection.radial_component
        elif instantaneous_measurement_direction_value == 3:
            instantaneous_measurement_direction = InstantaneousMeasurementDirection.lateral_component

        byte_offset = 1

        cumulative_crank_revs = None
        last_crank_event_time = None
        first_crank_measurement_angle = None
        instantaneous_force_magnitudes = []
        instantaneous_torque_magnitudes = []

        if crank_revolutions_present:
            cumulative_crank_revs = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2
            last_crank_event_time = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2

        if first_crank_measurement_angle_present:
            first_crank_measurement_angle = int.from_bytes(data[0 + byte_offset:2 + byte_offset], 'little')
            byte_offset += 2

        for i in range(byte_offset, len(data), 2):
            element = int.from_bytes(data[i:i + 2], 'little')

            if instantaneous_force_array_present:
                instantaneous_force_magnitudes.append(element)
            elif instantaneous_torque_array_present:
                instantaneous_torque_magnitudes.append(element)

        if self._cycling_power_vector_callback is not None:
            self._cycling_power_vector_callback(
                CyclingPowerVector(instantaneous_measurement_direction=instantaneous_measurement_direction,
                                   cumulative_crank_revs=cumulative_crank_revs,
                                   last_crank_event_time=last_crank_event_time,
                                   first_crank_measurement_angle=first_crank_measurement_angle,
                                   instantaneous_force_magnitudes=instantaneous_force_magnitudes,
                                   instantaneous_torque_magnitudes=instantaneous_torque_magnitudes))
