# ========== LIBRARIES ========== #
import json
import time
import network
import socket
import struct

import machine
import urequests
import utime

import _thread


# =============================== #

wnet = network.WLAN(network.STA_IF)
wnet.active(True)

# ========== NETWORK MGMT ========== #


class EspNet:
    def connect_network(w):
        def connect_to_wifi(w):
            # First check if there already is any connection:
            if wnet.isconnected():
                return wnet

            try:
                wnet.disconnect()
                time.sleep(1)

                # ESP connecting to WiFi takes time, wait a bit and try again:
                if wnet.isconnected():
                    return wnet

                # Search WiFis in range
                networks = wnet.scan()
                ssid = w['ssid']
                pw = w['password']

                print(f"networks: {networks}")
                print('connecting to network...')
                print(f"{ssid} - {pw}")

                wnet.connect(ssid, w['password'])
                print("Connecting.", end="")
                while not wnet.isconnected():
                    print(".", end="")
                    utime.sleep_ms(1000)

            except OSError as e:
                print("exception", str(e))

            print('Connected!')
            print('Network Config:', wnet.ifconfig())

        connect_to_wifi(w)


class Train(object):
    """Train Object Definition Class"""

    line: str = ''
    dest: str = ''
    minutes: str = ''

    def __init__(self, line, dest, min) -> None:
        self.line = line
        self.dest = dest
        self.min = min

    def __repr__(self) -> str:
        real_repr: str
        std_repr = f"{self.line} line to {self.dest}: {self.min}"

        try:
            _ = int(self.min)
            real_repr = std_repr + "m"

        # Quack
        except ValueError:
            # Use duck typing to infer non-minute values; these shouldn't
            #   be followed by the 'm' time remaining indication
            real_repr = std_repr

        return real_repr


#
class Wmata:
    """WMATA Class: Responsible for Running the Program: Connection, Data Fetching, and Display"""

    # Read JSON
    def load_config():
        # Load configuration
        f = open("config.json", "r")
        return json.load(f)

    def run():
        config = Wmata.load_config()
        wifi_settings = config['wifi'][0]
        api_key = config['wmata_api'][0]['public_key']
        station_code = config['wmata_api'][0]['station_code']
        station_predictions_url = f"https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{station_code}"

        EspNet.connect_network(wifi_settings)

        while True:
            res = urequests.get(station_predictions_url, headers={
                "api_key": api_key}).json()

            trains = []
            trains_json = res.get("Trains")

            # Ensure the response has the valid data we want
            if len(res) < 1:
                print("Got an empty response; trying again")
                utime.sleep_ms(500)
                continue

            # Create Objects from the returned JSON
            try:
                for train in trains_json:
                    trains.append(
                        Train(train['Line'], train['DestinationName'], train['Min']))

            except TypeError as e:
                print(f"Caught TypeError ({e}):\ntrains_json: {trains_json}")
                return

            # Display when trains will arrive:
            print("")
            for train in trains:
                print(f"{train}")

            print("")
            utime.sleep(10)
