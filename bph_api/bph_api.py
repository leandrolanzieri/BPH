import yaml
from datetime import datetime
from debug_pin import DebugPin
from heartbeat import HeartBeat
from power_management import PowerManagement
from time import sleep
import wiringpi as wpi

class BPH_API():
    def __init__(self, conf_path='../BPH-1A/bph_conf.yaml'):
        with open(conf_path) as f:
            conf = f.read()

        self.hat_conf = yaml.load(conf)
        self.gpio_conf = self.hat_conf['bph']['configuration']['gpio']

        # create heartbeat pin
        self.heartbeat = HeartBeat(self.gpio_conf['heartbeat']['pin'], \
                                   'heartbeat')
        # create debug pins
        self.debug_pins = []
        for idx, debug in enumerate(self.gpio_conf['debug']):
            self.debug_pins.append(DebugPin(debug['pin'],'DUT_out', 'debug ' \
                                                                    + str(idx)))

        # initialize BP reset as input, so BP can reset itself
        wpi.pinMode(self.gpio_conf['bp_rst']['pin'], wpi.GPIO.INPUT)

        # initialize power management module
        self.power_management = PowerManagement( \
                    self.gpio_conf['usb_en']['pin'],\
                    self.gpio_conf['ext_v_en']['pin'],
                    self.hat_conf['power_measurement']['shunt'])

    def debug_pin_set_mode(self, pin_number, mode):
        """Sets the mode for a debug pin.
            
        Args:
            pin_number (int): Number of the debug pin.
            mode (str): Mode of the pin. Any of 'RPI_out', 'DUT_out', 'BP_out'
        """
        self.debug_pins[pin_number].set_pin_mode(mode)
        return self._build_response('debug_pin_set_mode({}, {})' \
                                    .format(pin_number, mode), \
                                    None, 'SUCCESS')

    def debug_pin_set_state(self, pin_number, state):
        """Sets the state of a debug pin. Note that this can only be done when a
        pin is in 'RPI_out' mode.

        Args:
            pin_number (int): Number of the debug pin.
            state (int): State for the pin, either 'high' or 'low'.
        """
        self.debug_pins[pin_number].set_pin_state(state)
        return self._build_response('debug_pin_set_state({},{})' \
                                    .format(pin_number, state), \
                                    None, 'SUCCESS')

    def debug_pin_get_state(self, pin_number):
        """Returns the current state of a debug pin.

        Args:
            pin_number (int): Number of debug pin.
        """
        data = self.debug_pin_get_info(pin_number)['state']
        return self._build_response('debug_pin_get_state({}' \
                                    .format(pin_number), \
                                    None, 'SUCCESS')

    def debug_pin_get_info(self, pin_number):
        """Returns information about a specific debug pin.

            Args:
                pin_number (int): Number of the debug pin.
        """
        data = self.debug_pins[pin_number].get_gpio_info()
        return self._build_response('debug_pin_get_info({})' \
                                    .format(pin_number), \
                                    data, 'SUCCESS')

    def bp_hb_get_state(self):
        """Returns the current state of the heartbeat pin.
        """
        data = self.heartbeat.get_state()
        return self._build_response('bp_hb_get_state()', data, 'SUCCESS')

    def bp_hb_get_last(self):
        """Returns a timestamp with the last known heartbeat.
        """
        data = self.heartbeat.get_last()
        return self._build_response('bp_hb_get_last()', data, 'SUCCESS')

    def bp_hb_is_alive(self, min_time_s=1):
        """Verifies if the blue pill is alive by verifying the time of the last
        heartbeat.

        Args:
            min_time_s (int, optional): Minimum seconds since last heartbeat

        Returns:
            bool: True if is alive. False otherwise.
        """
        data = self.heartbeat.is_alive(min_time_s)
        return self._build_response('bp_hb_is_alive({})'.format(min_time_s),
                                    data, 'checking if BP is there', 'SUCCESS')

    def bp_reset(self, sleep_ms = 10):
        """Perfoms a reset on the blue pill board for an specified time.

        Args:
            sleep_ms (int, optional): Amount of time to reset the blue pill
                expressed in milliseconds.
        """
        wpi.pinMode(self.gpio_conf['bp_rst']['pin'], wpi.GPIO.OUTPUT)
        wpi.digitalWrite(self.gpio_conf['bp_rst']['pin'], wpi.GPIO.LOW)
        sleep(sleep_ms / 1000)
        wpi.pinMode(self.gpio_conf['bp_rst']['pin'], wpi.GPIO.INPUT)

        return self._build_response('bp_reset({})'.format(sleep_ms), None, \
                                    'SUCCESS')

    def dut_reset_soft(self, sleep_ms = 10):
        raise NotImplementedError

    def dut_reset_hard(self, sleep_ms = 10):
        """Cycles power to the DUT.

        Args:
            sleep_ms (int, optional): Amount of time to reset the DUT
                expressed in milliseconds.
        """
        self.power_management.set_power_state('OFF')
        sleep(sleep_ms / 1000)
        self.power_management.set_power_state('ON')
        return self._build_response('dut_reset_hard({})'.format(sleep_ms), \
                                    None, 'SUCCESS')

    def reset_full(self, sleep_ms = 100):
        """Performs a guaranteed power reset for the DUT and the blue pill
        board.

        Args:
            sleep_ms (int, optional): Amount of time to reset the DUT and
                the blue pill board.
        """
        wpi.pinMode(self.gpio_conf['bp_rst']['pin'], wpi.GPIO.OUTPUT)
        wpi.digitalWrite(self.gpio_conf['bp_rst']['pin'], wpi.GPIO.LOW)
        self.power_management.set_power_state('OFF')
        sleep(sleep_ms / 1000)
        self.power_management.set_power_state('ON')
        wpi.pinMode(self.gpio_conf['bp_rst']['pin'], wpi.GPIO.INPUT)

        return self._build_response('reset_full({})'.format(sleep_ms), \
                                    None, 'SUCCESS')

    def dut_power_set_conf(self, conf):
        """Sets the power configuration (i.e. the power source) for the DUT.

        Args:
            conf (string): Power configuration to be applied. 'USB' of 'EXT'
        """
        self.power_management.set_power_conf(conf)
        return self._build_response('dut_power_set_conf({})'.format(conf), \
                                    None, 'SUCCESS')

    def dut_power_get_conf(self):
        """Returns the current power configuration (i.e. the power source) for
        the DUT.
        """
        data = self.power_management.power_conf
        return self._build_response('dut_power_get_conf()', data, 'SUCCESS') 

    def dut_reset_soft(self, sleep_ms = 10):
        raise NotImplementedError

    def _build_response(self, cmd, data, result, msg = ''):
        """Returns a formatted response according to the Philip Test specs.

        Args:
            cmd (str): Executed command, including arguments
            data (any): Information received from the command
            result (str): Result of the command. Any of 'SUCCESS', 'ERROR',
                'TIMEOUT'.
            msg (str, optional): Result of the execution of the command
        """
        assert result in ('SUCCESS', 'ERROR', 'TIMEOUT'), \
                          'Invalid result: {}'.format(result)
        res = {}
        res['cmd'] = cmd
        res['data'] = data
        res['msg'] = msg
        res['result'] = result
    
        return res
