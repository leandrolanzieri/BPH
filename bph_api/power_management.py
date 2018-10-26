import wiringpi as wpi
from time import sleep
from driver_ina226 import INA226

class PowerManagement:

    def __init__(self, usb_pin, ext_pin, bp_rst_pin, measurement_shunt,
                 conf = 'USB'):
        # set power enable lines as outputs
        wpi.pinMode(usb_pin, wpi.GPIO.OUTPUT)
        wpi.pinMode(ext_pin, wpi.GPIO.OUTPUT)

        self.usb_pin = usb_pin
        self.ext_pin = ext_pin
        self.set_power_conf(conf)
        self.bp_rst_pin = bp_rst_pin
        self.shunt = measurement_shunt

        self.meas_dev = INA226(0x44, INA226.MODE_SHUNT_BUS_CONTINUOUS,
                               shunt_val = self.shunt)

    def set_power_conf(self, conf):
        assert conf in ('USB', 'EXT'), "Invalid power configuration '{}'"\
                                       .format(conf)
        self.power_conf = conf

        # check what pin needs to be turn on and which off
        on, off = [self.usb_pin, self.ext_pin] if conf == 'USB' else \
                  [self.ext_pin, self.usb_pin]
        
        wpi.digitalWrite(off, wpi.GPIO.LOW)
        wpi.digitalWrite(on, wpi.GPIO.HIGH)

    def set_power_state(self, state):
        assert state in ('ON', 'OFF'), "Invalid power state '{}'".format(state)

        _state = wpi.GPIO.HIGH if state == 'ON' else wpi.GPIO.LOW

        if self.power_conf == 'USB':
            wpi.digitalWrite(self.usb_pin, _state)
        else:
            wpi.digitalWrite(self.ext_pin, _state)

    def get_power_measurement(self):
        # measurements must be done with external power
        prev_conf = self.power_conf
        self.set_power_conf('EXT')

        prev_mode = wpi.getAlt(self.bp_rst_pin)
        prev_state = wpi.digitalRead(self.bp_rst_pin)

        # reset blue pill so power is not drained from gpios
        wpi.pinMode(self.bp_rst_pin, wpi.GPIO.OUTPUT)
        wpi.digitalWrite(self.bp_rst_pin, wpi.GPIO.LOW)

        # wait for a full conversion time
        # this may change if average on INA226 is increased
        sleep(2.2 / 1000)

        voltage = self.meas_dev.get_shunt_voltage()
        current = self.meas_dev.get_current()
        power = self.meas_dev.get_power()

        # restore the blue pill to previous state
        wpi.pinMode(self.bp_rst_pin, prev_mode)
        wpi.digitalWrite(self.bp_rst_pin, prev_state)

        # restore power configuration to previous state
        self.set_power_conf(prev_conf)

