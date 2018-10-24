from time import sleep
from bph_api import BPH_API as bph

if __name__ == '__main__':
    hat = bph()

    while True:
        hat.bp_reset()
        sleep(1)
        print(hat.bp_hb_is_alive())
