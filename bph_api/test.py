from time import sleep
from bph_api import BPH_API as bph

if __name__ == '__main__':
    hat = bph()

    print(hat.dut_power_set_conf('USB'))
    
    while True:
        print(hat.bp_hb_get_last())
