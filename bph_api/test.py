from time import sleep
from bph_api import BPH_API as bph

if __name__ == '__main__':
    hat = bph()
    hat.dut_power_set_conf('USB')
    
    while True:
        print("Reset Hard")
        hat.dut_reset_hard(sleep_ms = 50)
        sleep(5)

