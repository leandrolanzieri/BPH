from gpio_monitor import GpioMonitor
from datetime import datetime

class HeartBeat(GpioMonitor):
    def __init__(self, gpio, name = '', log_enable = True, log_buffer = 1024):
        super().__init__(gpio, 'INPUT', name, log_enable, log_buffer)

    def is_alive(self, min_time_s = 1):
        delta = datetime.now() - self.gpio['last_event']['time']
        return delta.total_seconds() <= min_time_s

    def get_state(self):
        return self.get_gpio_info()['state']

    def get_last(self):
        return self.gpio['last_event']['time']
