from gpio_monitor import GpioMonitor

class DebugPin(GpioMonitor):
    RPI_out = 0
    BP_out = 1
    DUT_out = 2

    def __init__(self, gpio, pin_mode, name = '', log_enable = True,
                 log_buffer = 1024):
        mode = 'output' if pin_mode == self.RPI_out else 'input'
        super().__init__(gpio, mode, name, log_enable, log_buffer)
        self.set_pin_mode(pin_mode)

    def set_pin_mode(self, mode):
        if mode == self.RPI_out:
            self.pin_mode = mode
            super().set_gpio_mode('output')
        else: 
            super().set_gpio_mode('input')
            self.pin_mode = mode

    def set_pin_state(self, state):
        # a chenge of state can only happen in RPI_out mode
        if self.mode == self.RPI_out:
            self.set_gpio_state(state)
    
