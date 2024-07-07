# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()

# from wmata import Wmata
from main import EspKw, EspNet
import ugit

EspNet.connect_network()
ugit.pull_all(isconnected=True)

# Pull single file:
# ugit.pull('file_name.ext', 'Raw_github_url')

EspKw.run()

# import upip
# upip.install('micropython-uasyncio')
