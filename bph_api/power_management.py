import wiringpi as wpi

class PowerManagement:

    def __init__(self, usb_pin, ext_pin, conf = 'USB'):
        # set power enable lines as outputs
        wpi.pinMode(usb_pin, wpi.GPIO.OUTPUT)
        wpi.pinMode(ext_pin, wpi.GPIO.OUTPUT)

        self.usb_pin = usb_pin
        self.ext_pin = ext_pin
        self.set_power_conf(conf)

    def set_power_conf(self, conf):
        assert conf in ('USB', 'EXT'), "Invalid power configuration '{}'"\
                                       .format(conf)
        self.power_conf = conf

        # check what pin needs to be turn on and which off
        on, off = [self.usb_pin, self.ext_pin] if conf == 'USB' else
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

    
