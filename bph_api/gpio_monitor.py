import wiringpi as wpi
from datetime import datetime
import collections

class GpioMonitor():
    def __init__(self, gpio, mode, name = '', log_enable = False,
                 log_buffer = 1024):
        wpi.wiringPiSetupGpio()
        self._register_gpio(gpio, mode, name, log_enable, log_buffer)

    def get_gpio_info(self):
        self.gpio['state'] = wpi.digitalRead(self.gpio['gpio'])
        return self.gpio

    def set_gpio_state(self, state):
        assert state in ('LOW', 'HIGH'), 'Invalid GPIO state {}' \
                                             .format(state)
        if self.gpio['mode'] == 'OUTPUT':
            previous = 'HIGH' if wpi.digitalRead(self.gpio['gpio']) else 'LOW'
            wpi.digitalWrite(self.gpio['gpio'], state == 'HIGH')

    def set_gpio_mode(self, mode):
        assert mode in ('OUTPUT', 'INPUT')
        # check correct mode
        if mode == 'OUTPUT':
            self._set_gpio_output()
        else:
            self._set_gpio_input()

    def _register_gpio(self, gpio, mode, name = '', log_enable = True,
                       log_buffer = 1024):
        name = str(gpio) if name == '' else name
        self.log_buffer = log_buffer
        self.log_enable = log_enable
        self.gpio = {'name': name, 'gpio': gpio}
        self.gpio['events'] = collections.deque(maxlen=log_buffer)
        self.gpio['mode'] = None

        # register the callback before setting the mode, otherwise it
        # won't work
        wpi.wiringPiISR(self.gpio['gpio'], wpi.GPIO.INT_EDGE_BOTH,
                        self._state_change_cb)

        if mode == 'INPUT':
            self._set_gpio_input()
        else:
            self._set_gpio_output()

    def _set_gpio_input(self):
        if self.gpio['mode'] != 'INPUT':
            self.gpio['mode'] = 'INPUT'
            wpi.pinMode(self.gpio['gpio'], wpi.GPIO.INPUT)
            self._log_event('MODE_CHANGE')

    def _set_gpio_output(self):
        print('Setting ' + self.gpio['name'] + ' as output')
        if self.gpio['mode'] != 'OUTPUT':
            self.gpio['mode'] = 'OUTPUT'
            wpi.pinMode(self.gpio['gpio'], wpi.GPIO.OUTPUT)
            self._log_event('MODE_CHANGE')

    def _state_change_cb(self):
        type = 'RAISE' if wpi.digitalRead(self.gpio['gpio']) else 'FALL'
        self._log_event(type)
    
    def _log_event(self, type):
        event = {'time': datetime.now(), 'type': type,
                 'mode': self.gpio['mode']}
        self.gpio['last_event'] = event

        if self.log_enable:
            self.gpio['events'].append(event)

