import smbus
from time import sleep

class INA226():
    # Regiter map
    REG_CONFIGURATION = 0x00
    REG_SHUNT_VOLTAGE = 0x01
    REG_BUS_VOLTAGE = 0x02
    REG_POWER = 0x03
    REG_CURRENT = 0x04
    REG_CALIBRATION = 0x05
    REG_MASK = 0x06
    REG_ALERT_LIMIT = 0x07
    REG_MANUFACTURER_ID = 0xFE
    REG_DIE_ID = 0xFF

    # Configuration register masks
    CONF_MASK_MODE = 0x0007
    CONF_MASK_SHUNT_CONV_TIME = 0x0038
    CONF_MASK_BUS_CONV_TIME = 0x01C0
    CONF_MASK_AVG = 0X0E00
    CONF_MASK_RST = 0X8000

    # Configuration register offsets
    CONF_OFFSET_MODE = 0
    CONF_OFFSET_SHUNT_CONV_TIME = 3
    CONF_OFFSET_BUS_CONV_TIME = 6
    CONF_OFFSET_AVG = 9
    CONF_OFFSET_RST = 15

    # Operation modes
    MODE_POWER_DOWN = 0
    MODE_SHUNT_TRIGGERED = 1
    MODE_BUS_TRIGGERED = 2
    MODE_SHUNT_BUS_TRIGGERED = 3
    #MODE_POWER_DOWN = 4
    MODE_SHUNT_CONTINUOUS = 5
    MODE_BUS_CONTINUOUS = 6
    MODE_SHUNT_BUS_CONTINUOUS = 7

    # Valid average values
    AVG_1 = 0
    AVG_4 = 1
    AVG_16 = 2
    AVG_64 = 3
    AVG_128 = 4
    AVG_256 = 5
    AVG_512 = 6
    AVG_1024 = 7

    def __init__(self, address, operation_mode, shunt_val = 1, bus_num = 1):
        self.bus = smbus.SMBus(bus_num)
        self.address = address
        self.shunt = shunt_val

    def _swap_16(self, word):
        return (((word >> 8) & 0x00FF) | ((word << 8) & 0xFF00))

    def _write_register(self, reg, value):
        value = self_swap_16(value)
        self.bus.write_word_data(self.address, reg, value)

    def _read_register(self, reg):
        data = self.bus.read_word_data(self.address, reg)
        return self._swap_16(data)

    def _set_configuration(self, value, mask, offset):
        conf = self._read_register(self.REG_CONFIGURATION)
        reg = (conf & ~(mask))
        reg |= (value << offset) & mask
        self._write_register(self.REG_CONFIGURATION, reg)

    def set_operation_mode(self, mode):
        assert mode in range(self.MODE_POWER_DOWN, self.SHUNT_BUS_CONTINUOUS),\
            'Invalid mode {}'.format(mode)
        self._set_configuration(mode, self.CONF_MASK_MODE, \
                                self.CONF_OFFSET_MODE)

    def set_avg(self, average):
        assert average in range(self.AVG_1, self.AVG1024), \
            'Invalid average {}'.format(average)

        self._set_configuration(average, self.CONF_MASK_AVG, \
                                self.CONF_OFFSET_AVG)

    def get_die_id(self):
        return self._read_register(self.REG_DIE_ID)

    def get_shunt_voltage(self):
        data = self._read_register(self.REG_SHUNT_VOLTAGE)
        # LSB = 2.5 uV
        return data * 2.5e-3 # in mV

    def get_bus_voltage(self):
        data = self._read_register(self.REG_SHUNT_VOLTAGE)
        # LSB = 1.25 mV
        return data * 1.25 # in mV

    def get_current(self):
        # TODO Use calibration registers instead of calculating current
        self.last_shunt_v = self.get_shunt_voltage()
        self.last_bus_v = self.get_bus_voltage()
        return (self.last_bus_v - self.last_shunt_v) / self.shunt

    def get_power(self):
        current = self.get_current()
        return current * self.last_shunt_v

if __name__ == '__main__':
    print('Testing INA226 connection')
    shunt = 39e3 # 39K
    dev = INA226(0x44, INA226.MODE_SHUNT_BUS_CONTINUOUS, shunt_val = shunt)

    while True:
        print('ID: {:02x}'.format(dev.get_die_id()))
        print('BUS: {}'.format(dev.get_bus_voltage()))
        print('SHUNT: {}'.format(dev.get_shunt_voltage()))
        print('CURRENT: {}'.format(dev.get_current()))
        sleep(2)
