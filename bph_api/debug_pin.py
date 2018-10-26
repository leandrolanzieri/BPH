from gpio_monitor import GpioMonitor

class DebugPin(GpioMonitor):
    def __init__(self, gpio, pin_mode, name = '', log_enable = True,
                 log_buffer = 1024):
        mode = 'OUTPUT' if pin_mode == 'RPI_out' else 'INPUT'
        super().__init__(gpio, mode, name, log_enable, log_buffer)
        self.set_pin_mode(pin_mode)

    def set_pin_mode(self, mode):
        assert mode in ('RPI_out', 'DUT_out', 'BP_out'), \
                        'Invalid debug pin mode {}'.format(mode)
        self.pin_mode = mode

        if mode == 'RPI_out':
            super().set_gpio_mode('OUTPUT')
        else: 
            super().set_gpio_mode('INPUT')

    def set_pin_state(self, state):
        assert self.pin_mode == 'RPI_out', ('A state can only be set when the '
                                            'debug pin is in "RPI_out" mode')

        # a change of state can only happen in RPI_out mode
        self.set_gpio_state(state)
