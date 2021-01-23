import binascii
from collections import namedtuple
from enum import Enum

# The GATT Characteristic used for sending FE-C messages to Tacx trainer
tacx_uart_rx_id = '6e40fec3-b5a3-f393-e0a9-e50e24dcca9e'
# The GATT Characteristic used for receiving FE-C messages from Tacx trainer
tacx_uart_tx_id = '6e40fec2-b5a3-f393-e0a9-e50e24dcca9e'

EquipmentType = Enum('EquipmentType', 'treadmill elliptical reserved rower climber nordic_skier trainer')

FEState = Enum('FEState', 'reserved ready in_use finished')

TargetPowerLimit = Enum('TargetPowerLimit',
                        'operating_at_target_or_no_target_set user_speed_too_low user_speed_too_high limit_reached')

CommandStatus = Enum('CommandStatus', 'success fail not_supported rejected uninitialized')


class RoadSurface(Enum):
    """
    Road surfaces supported by the NEO road feel feature
    """
    SIMULATION_OFF = 0
    CONCRETE_PLATES = 1
    CATTLE_GRID = 2
    COBBLESTONES_HARD = 3
    COBBLESTONES_SOFT = 4
    BRICK_ROAD = 5
    OFF_ROAD = 6
    GRAVEL = 7
    ICE = 8
    WOODEN_BOARDS = 9


GeneralFEData = namedtuple('GeneralFEData',
                           ['equipment_type', 'elapsed_time', 'distance_travelled', 'speed', 'heart_rate', 'fe_state',
                            'lap_toggle'])

SpecificTrainerData = namedtuple('SpecificTrainerData',
                                 ['update_event_count', 'instantaneous_cadence', 'accumulated_power',
                                  'instantaneous_power', 'trainer_status', 'target_power_limits', 'fe_state',
                                  'lap_toggle', 'power_calibration_required', 'resistance_calibration_required',
                                  'user_configuration_required'])

CommandStatusData = namedtuple('CommandStatusData', ['last_received_command', 'command_status', 'data'])


class TacxTrainerControl:
    def __init__(self, client):
        self._client = client
        self._general_fe_data_page_callback = None
        self._specific_trainer_data_page_callback = None
        self._command_status_data_page_callback = None

    async def set_basic_resistance(self, resistance):
        """Activate basic resistance mode, with specified resistance

        :param resistance: Resistance to apply to trainer, in newtons
        """
        if resistance < 0 or resistance > 200:
            raise ValueError('resistance must be between 0 and 200')

        write_value = bytearray([0xA4, 0x09, 0x4F, 0x05, 0x30, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        write_value.append(int((resistance / 200) * 200))
        await self._send_fec_cmd(write_value)

    async def set_target_power(self, target_power):
        """Activate target power mode, with specified target power

        :param target_power: Target power, in watts
        """
        if target_power < 0 or target_power > 4000:
            raise ValueError('target_power must be between 0 and 4000')

        write_value = bytearray([0xA4, 0x09, 0x4F, 0x05, 0x31, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        target_power_bytes = int(target_power / 0.25).to_bytes(2, byteorder='little')
        write_value.append(target_power_bytes[0])
        write_value.append(target_power_bytes[1])
        print(write_value)
        await self._send_fec_cmd(write_value)

    async def set_wind_resistance(self, wind_resistance_coefficient, wind_speed, drafting_factor):
        """Activate simulation mode, specifying wind parameters

        :param wind_resistance_coefficient: Wind resistance coefficient is the product of the frontal surface area,
            drag coefficient and air density of the simulation, in kg/m
        :param wind_speed: Speed of wind acting on cyclist in simulation, in km/h. A positive value represents a head
            wind while a negative value represents a tail wind
        :param drafting_factor: Use parameter to scale wind resistance to simulate drafting behind a virtual opponent
        """
        if wind_resistance_coefficient < 0 or wind_resistance_coefficient > 1.86:
            raise ValueError('wind_resistance_coefficient must be between 0 and 1.86')

        if wind_speed < -127 or wind_speed > 127:
            raise ValueError('wind_speed must be between -127 and 127')

        if drafting_factor < 0 or drafting_factor > 1:
            raise ValueError('drafting_factor must be between 0 and 1')

        write_value = bytearray([0xA4, 0x09, 0x4F, 0x05, 0x32, 0xFF, 0xFF, 0xFF, 0xFF])
        write_value.append(int(wind_resistance_coefficient / 0.01))
        write_value.append(int(wind_speed + 127))
        write_value.append(int(drafting_factor / 0.01))
        await self._send_fec_cmd(write_value)

    async def set_track_resistance(self, grade, coefficient_of_rolling_resistance):
        """Activate simulation mode, specifying track resistance parameters

        :param grade: The grade (slope) of simulated track, in %.
        :param coefficient_of_rolling_resistance: The coefficient of rolling resistance, in dimensionless units
        """
        if grade < -200 or grade > 200:
            raise ValueError('grade must be between -200 and 200')

        if coefficient_of_rolling_resistance < 0 or coefficient_of_rolling_resistance > 0.0127:
            raise ValueError('coefficient_of_rolling_resistance must be between 0 and 0.0127')

        write_value = bytearray([0xA4, 0x09, 0x4F, 0x05, 0x33, 0xFF, 0xFF, 0xFF, 0xFF])
        grade_bytes = int((grade + 200) / 0.01).to_bytes(2, byteorder='little')
        write_value.append(grade_bytes[0])
        write_value.append(grade_bytes[1])
        write_value.append(int(coefficient_of_rolling_resistance / 5e-5))
        await self._send_fec_cmd(write_value)

    async def set_user_configuration(self, user_weight, bicycle_weight,
                                     bicycle_wheel_diameter, gear_ratio):
        """Configure trainer parameters, used when the trainer is in simulation mode

        :param user_weight: Weight of the user in kilograms
        :param bicycle_weight: Weight of bicycle in kilograms
        :param bicycle_wheel_diameter: Diameter of bike wheel, in metres
        :param gear_ratio: The bike gear ratio (front chain ring teeth:rear wheel cog teeth)
        """
        if user_weight < 0 or user_weight > 655.34:
            raise ValueError('user_weight must be between 0 and 655.34')

        if bicycle_weight < 0 or bicycle_weight > 50:
            raise ValueError('bicycle_weight must be between 0 and 50')

        if bicycle_wheel_diameter < 0 or bicycle_wheel_diameter > 2.54:
            raise ValueError('bicycle_wheel_diameter must be between 0 and 2.54')

        if gear_ratio < 0.03 or gear_ratio > 7.65:
            raise ValueError('gear_ratio must be between 0.03 and 7.65')

        write_value = bytearray([0xA4, 0x09, 0x4F, 0x05, 0x37])

        user_weight_bytes = int(user_weight / 0.01).to_bytes(2, byteorder='little')
        write_value.append(user_weight_bytes[0])
        write_value.append(user_weight_bytes[1])
        write_value.append(0xff)
        bicycle_wheel_diameter_offset = int(round((bicycle_wheel_diameter - round(bicycle_wheel_diameter, 2)) / 0.001))
        bicycle_weight_bytes = int(bicycle_weight / 0.05).to_bytes(2, byteorder='little')
        write_value.append(bicycle_wheel_diameter_offset + ((bicycle_weight_bytes[0] << 4) & 0xff))
        write_value.append((bicycle_weight_bytes[0] >> 4) + (bicycle_weight_bytes[1] << 4))
        write_value.append(int(round(bicycle_wheel_diameter, 2) / 0.01))
        write_value.append(int(gear_ratio / 0.03))
        await self._send_fec_cmd(write_value)

    async def set_neo_modes(self, isokinetic_mode=False, isokinetic_speed=4.2,
                            road_surface_pattern=RoadSurface.SIMULATION_OFF,
                            road_surface_pattern_intensity=255):
        """Set NEO specific parameters such as Road Feel mode and Isokinetic training mode

        :param isokinetic_mode: Enable isokinetic mode of the trainer
        :param isokinetic_speed: The target speed used in isokinetic mode
        :param road_surface_pattern: The road surface to be simulated
        :param road_surface_pattern_intensity: The intensity of the feeling of the road surface. Note that even 50%
            feels fairly intense, 100% is untested and may damage the trainer!
        """
        if isokinetic_speed < 4.2 or isokinetic_speed > 8.4:
            raise ValueError('isokinetic_speed must be between 4.2 and 8.4')

        if road_surface_pattern_intensity != 255 and (
                road_surface_pattern_intensity < 0 or road_surface_pattern_intensity > 100):
            raise ValueError('road_surface_pattern_intensity must be between 0 and 100, or set to 255')

        write_value = bytearray([0xA4, 0x09, 0x4F, 0x05, 0xFC, 0x00])
        if isokinetic_mode:
            write_value.append(1)
            write_value.append(int(isokinetic_speed / 0.05))
        else:
            write_value.append(0x00)
            write_value.append(0x00)

        write_value.append(0)
        write_value.append(road_surface_pattern.value)
        write_value.append(road_surface_pattern_intensity)
        write_value.append(0x00)
        await self._send_fec_cmd(write_value)

    async def request_data_page(self, page_number):
        write_value = bytearray([0xA4, 0x09, 0x4F, 0x05, 0x46, 0xFF, 0xFF, 0xFF, 0xFF, 0x80])
        write_value.append(page_number)
        write_value.append(0x01)
        await self._send_fec_cmd(write_value)

    def set_general_fe_data_page_handler(self, callback):
        self._general_fe_data_page_callback = callback

    def set_specific_trainer_data_page_handler(self, callback):
        self._specific_trainer_data_page_callback = callback

    def set_command_status_data_page_handler(self, callback):
        self._command_status_data_page_callback = callback

    async def _send_fec_cmd(self, fec_bytes):
        checksum = sum(fec_bytes[1:]) & 0xFF
        fec_bytes.append(checksum)
        await self._client.write_gatt_char(tacx_uart_rx_id, fec_bytes)

    async def enable_fec_notifications(self):
        await self._client.start_notify(tacx_uart_tx_id, self._fec_notification_handler)

    async def disable_fec_notifications(self):
        await self._client.stop_notify(tacx_uart_tx_id)

    def _fec_notification_handler(self, sender, data):
        message_length = data[1]
        message_type = data[2]
        message_channel = data[3]
        message_data = data[4:4 + message_length - 1]
        data_page_no = message_data[0]

        print(f'recieved data page number: {data_page_no} message: {binascii.hexlify(message_data)}')

        if data_page_no == 16:
            self._general_fe_data_page_handler(message_data)
        elif data_page_no == 25:
            self._specific_trainer_data_page_handler(message_data)
        elif data_page_no == 71:
            self._command_status_data_page_handler(message_data)

    def _general_fe_data_page_handler(self, message_data):
        equipment_type_code = message_data[1]
        equipment_type = self._equipment_type_from_code(equipment_type_code)

        elapsed_time = message_data[2] * 0.25

        distance_traveled = message_data[3]

        speed_raw = int.from_bytes(message_data[4:6], 'little')
        speed = None
        if speed_raw != 65535:
            speed = speed_raw * 0.001

        heart_rate = message_data[6]
        if heart_rate == 255:
            heart_rate = None

        fe_state, lap_toggle = self._parse_fe_state_nibble((message_data[7] >> 4))

        if self._general_fe_data_page_callback is not None:
            self._general_fe_data_page_callback(GeneralFEData(equipment_type=equipment_type, elapsed_time=elapsed_time,
                                                              distance_travelled=distance_traveled, speed=speed,
                                                              heart_rate=heart_rate, fe_state=fe_state,
                                                              lap_toggle=lap_toggle))

    @staticmethod
    def _equipment_type_from_code(equipment_type_code):
        equipment_type = None
        if equipment_type_code == 19:
            equipment_type = EquipmentType.treadmill
        elif equipment_type_code == 20:
            equipment_type = EquipmentType.elliptical
        elif equipment_type_code == 21:
            equipment_type = EquipmentType.reserved
        elif equipment_type_code == 22:
            equipment_type = EquipmentType.rower
        elif equipment_type_code == 23:
            equipment_type = EquipmentType.climber
        elif equipment_type_code == 24:
            equipment_type = EquipmentType.nordic_skier
        elif equipment_type_code == 25:
            equipment_type = EquipmentType.trainer
        return equipment_type

    @staticmethod
    def _parse_fe_state_nibble(fe_state_nibble):
        lap_toggle = bool(fe_state_nibble & 0x8)
        code = fe_state_nibble & 0x7
        fe_state = None
        if code == 0:
            fe_state = FEState.reserved
        elif code == 1:
            fe_state = FEState.asleep
        elif code == 2:
            fe_state = FEState.ready
        elif code == 3:
            fe_state = FEState.in_use
        elif code == 4:
            fe_state = FEState.finished
        return fe_state, lap_toggle

    def _specific_trainer_data_page_handler(self, message_data):
        update_event_count = message_data[1]

        instantaneous_cadence = message_data[2]
        if instantaneous_cadence == 255:
            instantaneous_cadence = None

        accumulated_power = int.from_bytes(message_data[3:5], 'little')

        power_lsb = message_data[5]
        power_msb = message_data[6]
        instantaneous_power = power_lsb + ((power_msb & 0xf) << 8)

        if instantaneous_power == 4095:
            instantaneous_power = None

        trainer_status_flags = (power_msb >> 4) & 0xf

        power_calibration_required = bool(trainer_status_flags & 0x1)
        resistance_calibration_required = bool(trainer_status_flags & 0x2)
        user_configuration_required = bool(trainer_status_flags & 0x4)

        fe_state, lap_toggle = self._parse_fe_state_nibble((message_data[7] >> 4))
        target_power_limits = None

        flags = message_data[7] & 0x7

        if flags == 0:
            target_power_limits = TargetPowerLimit.operating_at_target_or_no_target_set
        elif flags == 1:
            target_power_limits = TargetPowerLimit.user_speed_too_low
        elif flags == 2:
            target_power_limits = TargetPowerLimit.user_speed_too_high
        elif flags == 3:
            target_power_limits = TargetPowerLimit.limit_reached

        if self._specific_trainer_data_page_callback is not None:
            self._specific_trainer_data_page_callback(
                SpecificTrainerData(update_event_count=update_event_count,
                                    instantaneous_cadence=instantaneous_cadence,
                                    accumulated_power=accumulated_power,
                                    instantaneous_power=instantaneous_power,
                                    trainer_status=None,
                                    target_power_limits=target_power_limits,
                                    fe_state=fe_state, lap_toggle=lap_toggle,
                                    power_calibration_required=power_calibration_required,
                                    resistance_calibration_required=resistance_calibration_required,
                                    user_configuration_required=user_configuration_required))

    def _command_status_data_page_handler(self, message_data):
        last_received_command = message_data[1]
        command_status = None
        command_status_byte = message_data[3]

        if command_status_byte == 0:
            command_status = CommandStatus.success
        elif command_status_byte == 1:
            command_status = CommandStatus.fail
        elif command_status_byte == 2:
            command_status = CommandStatus.not_supported
        elif command_status_byte == 3:
            command_status = CommandStatus.rejected
        elif command_status_byte == 255:
            command_status = CommandStatus.uninitialized

        if self._command_status_data_page_callback is not None:
            self._command_status_data_page_callback(
                CommandStatusData(last_received_command=last_received_command, command_status=command_status,
                                  data=message_data[4:8]))
