import yaml
from datetime import datetime
from debug_pin import DebugPin
from heartbeat import HeartBeat
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
            self.debug_pins.append(DebugPin(debug['pin'], 'debug ' + str(idx)))

        # initialize BP reset
        wpi.pinMode(self.gpio_conf['bp_rst']['pin'], wpi.GPIO.OUTPUT)

    def debug_pin_set_mode(self, pin_number, mode):
        """Sets the mode for a debug pin.
            Args:
                pin_number (int): Number of the debug pin.
                mode (int): One of the modes available in DebugPin class
                        -DebugPin.RPI_out
                        -DebugPin.BP_out
                        -DebugPin.DUT_out
        """
        self.debug_pins[pin_number].set_pin_mode(mode)

    def debug_pin_set_state(self, pin_number, state):
        """Sets the state of a debug pin. Note that this can only be done when a
           pin is in DebugPin.RPI_out mode.

           Args:
                pin_number (int): Number of the debug pin.
                state (int): State for the pin, either 'high' or 'low'.
        """
        self.debug_pins[pin_number].set_pin_state(state)

    def debug_pin_get_info(self, pin_number):
        """Returns information about a specific debug pin.

            Args:
                pin_number (int): Number of the debug pin.
        """
        return self.debug_pins[pin_number].get_gpio_info()

    def bp_hb_is_alive(self, min_time_s=1):
        """Verifies if the blue pill is alive by verifying the time of the last
        heartbeat.

            Args:
                min_time_s (int, optional): Minimum seconds since last heartbeat

            Returns:
                bool: True if is alive. False otherwise.
        """
        return self.heartbeat.is_alive(min_time_s)

    def bp_reset(self, sleep_ms = 10):
        """Perfoms a reset on the blue pill board for an specified amount of
        time.

            Args:
                sleep_ms (int, optional): Amount of time to reset the blue pill
                expressed in milliseconds.
        """
        wpi.digitalWrite(self.gpio_conf['bp_rst']['pin'], wpi.GPIO.LOW)
        sleep(sleep_ms / 1000)
        wpi.digitalWrite(self.gpio_conf['bp_rst']['pin'], wpi.GPIO.HIGH)
    
    def dut_reset_soft(self, sleep_ms = 10):
        pass

    def dut_reset_hard(self, sleep_ms = 10):
        # TODO this should be handled by the power management module
        prev_power_usb = wpi.digitalRead(self.gpio_conf['usb_en']
        
        if prev_power_usb:
            wpi.digitalWrite(self.gpio_conf['usb_en'], wpi.GPIO.LOW)
        else:
            wpi.digitalWrite(self.gpio_conf['ext_v_en'], wpi.GPIO.LOW)

        sleep(sleep_ms / 1000)

        if prev_power_usb:
            wpi.digitalWrite(self.gpio_conf['usb_en'], wpi.GPIO.HIGH)
        else:
            wpi.digitalWrite(self.gpio_conf['ext_v_en'], wpi.GPIO.HIGH)

        
