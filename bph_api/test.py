from time import sleep
from bph_api import BPH_API as bph
import pprint

if __name__ == '__main__':
    hat = bph()

    print(hat.dut_power_set_conf('USB'))
    sleep(2)
    print(hat.dut_power_set_conf('EXT'))
    print(hat.dut_power_get_conf())
    pp = pprint.PrettyPrinter()
    print(hat.debug_pin_set_mode(2, 'RPI_out'))
    while True:
        print(hat.debug_pin_set_state(2, 'HIGH'))
        sleep(0.1)
        print(hat.debug_pin_set_state(2, 'LOW'))
        sleep(0.1)
        pp.pprint(hat.debug_pin_get_info(2)['data']['events'])
        sleep(2)
