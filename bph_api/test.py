from time import sleep
from bph_api import BPH_API as bph
import pprint

if __name__ == '__main__':
    hat = bph()

    print(hat.dut_power_set_conf('USB'))
    sleep(2)

    while True:
        sleep(2)
        print(hat.dut_power_get_measurement())
