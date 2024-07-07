# ========== LIBRARIES ========== #
import json
import time
import network
import socket
import struct
import urequests
import uasyncio as asyncio

from utime import sleep, sleep_ms
from microdot import Microdot, Response
from microdot_utemplate import render_template

# from machine import I2C, Pin, UART
# from lcd.pico_i2c_lcd import I2cLcd
# from phew import logging, server, connect_to_wifi, is_connected_to_wifi, access_point
# from phew.template import render_template
import _thread


# =============================== #

# Display Cfg ======================== #

from machine import Pin, SoftI2C, RTC
from lcd.i2c_lcd import I2cLcd

COLS = 16
ROWS = 2

# I2C Pin Definitions
sda_pin = Pin(21)
scl_pin = Pin(22)

# Create an I2C Object out of our SCL and SDA Pin Ojbects
i2c = SoftI2C(scl=scl_pin, sda=sda_pin, freq=10000)
I2C_ADDR = i2c.scan()[0]

# "lcd" is the object with which we print to the display
lcd = I2cLcd(i2c, I2C_ADDR, ROWS, COLS)

enabled_taps = 0

# =============================== #

# Network Cfg ======================= #

wnet = network.WLAN(network.STA_IF)
wnet.active(True)

# =============================== #

# ========== CALIBRATION ========== #


def calibration_pour(t):
    global CAL_COUNT, CAL_MODE
    CAL_COUNT += 1

    # if CAL_COUNT < CAL_POURS:
    #     CAL_RATES.append(t)
    #     lcd.clear()
    # lcd.putstr(("Pour " + str(CAL_COUNT) + " of " + str(CAL_POURS)).center(COLS))
    # lcd.putstr(("Complete!").center(COLS))

    # else:
    #     CAL_RATES.append(t)
    #     CAL_MODE = False
    #     lcd.clear()
    #     lcd.putstr(("Pours Complete!").center(COLS))
    #     lcd.putstr(("See Web Portal").center(COLS))


def calibration_calc(p1, p2, p3, p4):
    global CAL_COUNT, CAL_POURED, CAL_TAP, CAL_RATES
    total_poured, flow_rate = 0, 0
    poured, pour_count = 0, 0

    if p1 != None:
        flow_rate += float(p1)/float(CAL_RATES[0])
        poured += float(p1)
        pour_count += 1
    if p2 != None:
        flow_rate += float(p2)/float(CAL_RATES[1])
        poured += float(p2)
        pour_count += 1
    if p3 != None:
        flow_rate += float(p3)/float(CAL_RATES[2])
        poured += float(p3)
        pour_count += 1
    if p4 != None:
        flow_rate += float(p4)/float(CAL_RATES[3])
        poured += float(p4)
        pour_count += 1

    flow_rate = flow_rate/pour_count
    beer_remaining = (float(taps[CAL_TAP]["remaining"]) - poured)

    # Update the config
    config = load_config()
    for item in config[("tap_"+str(CAL_TAP))]:
        item['flow_rate'] = flow_rate
        item['remaining'] = beer_remaining

    with open('config.json', 'w') as f:
        json.dump(config, f)

    # Report externally if required
    if int(mqtt_settings['status']) == 1:
        push_mqtt()
    if int(api_settings['status']) == 1:
        push_api(CAL_TAP, poured, "Calibration")

    CAL_COUNT, CAL_POURED, CAL_TAP = 0, 0, 0
    CAL_RATES = []
    # display_default()


def calibration_kickoff(t, n):
    global CAL_MODE, CAL_POURS, CAL_TAP
    CAL_MODE = True
    CAL_POURS = int(n)
    CAL_TAP = int(t)
    lcd.clear()
    lcd.putstr(("Calibrate Tap " + str(t)).center(COLS))
    lcd.putstr((str(n) + " Pours").center(COLS))
# ================================= #


# ========== WEB SERVER ========== #
web_server = Microdot()
Response.default_content_type = 'text/html'


@web_server.route('/')
def index(request):
    return render_template("html/index.html", title="KegWatch | Data by the Pint")

# server.add_route("/calibrate", configure_cal,["POST",'GET'])


@web_server.route('/calibrate', methods=['GET', 'POST'])
def configure_cal(req):
    print(req.method)
    if req.method == 'GET':
        return render_template("html/calibrate.html")
    if req.method == 'POST':
        selected_tap = req.form.get("select_tap", None)
        select_numpours = req.form.get("select_numpours", None)
        p1 = req.form.get("p1_amount", None)

        if p1 == None:
            calibration_kickoff(selected_tap, select_numpours)
            return render_template("html/calibrate"+select_numpours+".html")
        else:
            calibration_calc(req.form.get("p1_amount", None), req.form.get(
                "p2_amount", None), req.form.get("p3_amount", None), req.form.get("p4_amount", None))
            return render_template("html/default.html", content="Boom! System calibrated")

# @server.catchall()
# def my_catchall(request):
#     return "No matching route", 404


# ================================= #


# ========== DISPLAY MGMT ========== #
# String formatter
def format_str(s):
    target_length = COLS
    if len(s) > target_length:
        s = s[:target_length]
    elif len(s) < target_length:
        for x in range(target_length-len(s)):
            s += " "
    return s

# Default Display


def splash():
    h = bytearray([0x00, 0x00, 0x1B, 0x1F, 0x1F, 0x0E, 0x04, 0x00])
    lcd.clear()
    lcd.custom_char(0, h)
    lcd.putstr(("KegWatch " + chr(0)).center(COLS))


def display_default():
    config = load_config()

    # Configure display based on # of taps
    if enabled_taps == 0:
        lcd.clear()
        lcd.putstr("No Taps".center(COLS))
        lcd.putstr("Configured!".center(COLS))

    elif enabled_taps == 1:
        lcd.clear()
        lcd.putstr("Tap 1 Remaining".center(COLS))
        lcd.putstr((str(round(taps[1]["remaining"], 2)) + "oz").center(COLS))

    elif enabled_taps == 2:
        lcd.clear()
        lcd.putstr(format_str(
            ("Tap 1: " + str(round(taps[1]["remaining"], 2)) + "oz")))
        lcd.putstr(format_str(
            ("Tap 2: " + str(round(taps[2]["remaining"], 2)) + "oz")))

    elif enabled_taps == 3:
        lcd.clear()
        lcd.putstr(format_str(
            "1:" + str(round(taps[1]["remaining"]+"oz")) + "3:" + str(round(taps[3]["remaining"]+"oz"))))
        lcd.putstr(format_str("2:" + str(round(taps[2]["remaining"]+"oz"))))

# Show pouring status


def display_pouring(m, t, o):
    if m == 1:
        # Tap Open
        lcd.clear()
        if CAL_MODE:
            lcd.putstr(("Tap  " + str(t)).center(COLS))
            lcd.putstr("Calibration Pour")
        else:
            if consumer == "Anonymous":
                lcd.putstr(("Tap  " + str(t)).center(COLS))
                lcd.putstr("Pouring...".center(COLS))
            else:
                lcd.putstr(("Tap " + str(t) + " Pouring").center(COLS))
                if len(consumer) > COLS:
                    lcd.putstr(consumer.split(" ")[0].center(COLS))
                else:
                    lcd.putstr(consumer.center(COLS))

    elif m == 0:
        # Tap Closed
        lcd.clear()
        lcd.putstr("Pour Complete:".center(COLS))
        lcd.putstr((str(round(o, 2)) + "oz").center(COLS))

    elif m == 3:
        # Tap Closed
        lcd.clear()
        lcd.putstr("Inactive Tap".center(COLS))
        lcd.putstr(("No Beer Logged!").center(COLS))

# ================================== #


# ========== NETWORK MGMT ========== #

class EspNet:
    # Create local/ad-hoc network for setup
    def connect_to_wifi(w):
        # First check if there already is any connection:
        if wnet.isconnected():
            return wnet

        try:
            # ESP connecting to WiFi takes time, wait a bit and try again:
            if wnet.isconnected():
                return wnet

            # Search WiFis in range
            networks = wnet.scan()
            print(f"networks: {networks}")

            # Inform that you're connecting to a given network
            lcd.putstr("Connecting to:".center(COLS))
            lcd.clear()
            lcd.putstr(f"{w['ssid']}".center(COLS))
            print('connecting to network...')
            print(f"{w['ssid']} - {w['password']}")

            # Actually connect to the network
            wnet.connect(w['ssid'], w['password'])
            print("Connecting.", end="")
            while not wnet.isconnected():
                print(".", end="")
                sleep_ms(1000)

        except OSError as e:
            print("exception", str(e))

        print('Connected!')
        lcd.clear()
        lcd.putstr("Connected!")
        sleep(1)
        lcd.clear()

        print('Network Config:', wnet.ifconfig())

    def gen_ap():
        ap_ssid = "KegWatch"
        ap_pw = "123456789"

        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=ap_ssid, password=ap_pw)

        print("Serving ap.", end="")
        while not ap.active():
            print(".", end="")
            sleep(1)
            pass

        sleep(3)

    def connect_network():
        # Connect to network if it's provided
        config = Kw.instance().cfg
        wifi_settings = config['wifi'][0]
        if len(wifi_settings['ssid']) > 0:
            EspNet.connect_to_wifi(wifi_settings)
        else:
            EspNet.gen_ap()


# Return current time as string
def get_time():
    t = localtime()
    return (str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + " " + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5]))


# Get time via NTP
def set_time():
    NTP_DELTA = 2208988800
    host = "pool.ntp.org"

    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA
    tm = gmtime(t)
    RTC().datetime(
        (tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

# ================================== #


# ========== FUNCTIONS ========== #
# Read JSON
def load_config():
    # Load configuration
    f = open("config.json", "r")
    return json.load(f)


# Get input from barcode scanner
# def scan(pin):
#     if uart.any():
#         b = uart.read()
#     try:
#         msg = b.decode('utf-8')
#         global consumer
#         consumer = msg[:-1]
#     except:
#         pass


# Tap Handler
# def tap_pouring(pin):
#     # Variables for timer
#     global start
#     global stop

#     # Get Tap
#     # tap_id = list(tap_sensors.keys())[list(tap_sensors.values()).index(int((str(pin).split('('))[1][:2]))]
#     if pin == t1_sensor:
#         tap_id = 1
#     elif pin == t2_sensor:
#         tap_id = 2
#     elif pin == t3_sensor:
#         tap_id = 3

#     if pin.value() == 1:
#         # Tap is open - mark the time
#         start = time.ticks_ms()
#         # display_pouring(1,tap_id,0)

#     if pin.value() == 0:
#         # Tap is closed - mark the time
#         stop = time.ticks_ms()

#         # Calculate time tap was open
#         time_open = time.ticks_diff(stop, start)

#         # Calculate beer poured
#         if CAL_MODE:
#             calibration_pour(time_open)
#         else:
#             calc_beer(tap_id, time_open)


# Calculate Beer Poured
def calc_beer(t, s):
    taps = EspKw.get_taps()
    config = Kw.instance().cfg

    # Check to make sure the keg is active
    status = int(taps[t]["beer_status"])
    global consumer
    if status == 1:
        # Figure out beer poured/remaining
        beer_poured = (s * float(taps[t]["flow_rate"]))
        beer_remaining = (float(taps[t]["remaining"]) - beer_poured)
        display_pouring(0, t, beer_poured)

        # Don't let remaining go negative, negative beer is sad and impossible
        if beer_remaining <= 0:
            beer_remaining = 0
            status = 0

        # Update the config
        for item in config[("tap_"+str(t))]:
            item['remaining'] = beer_remaining

        with open('config.json', 'w') as f:
            json.dump(config, f)

        # Reset the consumer
        consumer = "Anonymous"

        # Report externally if required
        # if int(mqtt_settings['status']) == 1:
        #     push_mqtt()
        # if int(api_settings['status']) == 1:
        #     push_api(t, beer_poured, consumer)

        time.sleep(1)
        # display_default()
    else:
        display_pouring(3, t, 0)


def push_mqtt():
    pass


def push_api(t, p, c):
    # t = tap | p = poured | c = consumer
    payload = {
        'time': get_time(),
        'tap_id': t,
        'consumer': c,
        'oz_poured': p
    }

    try:
        response = urequests.post(api_host+"/beer", json=payload)
    except:
        lcd.clear()
        lcd.putstr("API Error!".center(COLS))
        lcd.putstr("Saving Locally".center(COLS))
        time.sleep(2)


def read_api():
    try:
        config = Kw.instance().cfg
        response = urequests.get(api_host+"/kegs").json()
        for x in range(len(response)):
            if response[x]['status'] == 1:
                # Update the config
                for item in config[("tap_"+str(response[x]['tap']))]:
                    if item['keg_id'] == response[x]['id'] and item['remaining'] < response[x]['remaining']:
                        difference = response[x]['remaining'] - \
                            item['remaining']
                        push_api(response[x]['tap'], difference, "Data Sync")
                    else:
                        item['keg_id'] = response[x]['id']
                        item['beer'] = response[x]['name']
                        item['capacity'] = response[x]['capacity']
                        item['remaining'] = response[x]['remaining']
                        item['beer_status'] = response[x]['status']

                with open('config.json', 'w') as f:
                    json.dump(config, f)

    except:
        lcd.clear()
        lcd.putstr("API Error!".center(COLS))
        lcd.putstr("Local Only".center(COLS))
        time.sleep(2)

# =============================== #


class Singleton:
    """Because some shit is just slow on microcontrollers (like reading in files)"""

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class Kw:
    cfg: dict

    def __init__(self):
        f = open("config.json", "r")
        self.cfg = json.load(f)


# ========== MAIN ========== #

class EspKw:
    # Tap configuration
    def get_taps():
        c = Kw.instance().cfg

        try:
            return {
                1: c['tap_1'][0],
                2: c['tap_2'][0],
                3: c['tap_3'][0]
            }
        except ValueError as e:
            print(f"{e}: the config provided: \n{c}\n")
            exit()

    def run():
        """Main function of the KegWatch sensor on ESP32"""
        splash()

        # Set consumer
        consumer = "Anonymous"

        # Load configs
        # config = Kw.instance().cfg

        lcd.clear()
        lcd.putstr(("KegWatch, BITCH!").center(COLS))

        sleep(60)
        lcd.clear()

        # Calibration mode parameters
        CAL_MODE = False
        CAL_COUNT, CAL_POURS, CAL_TAP = 0, 0, 0
        CAL_RATES = []

        # Configure barcode scanner
        # uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9),bits=8, parity=None, stop=1,txbuf=10,rxbuf=10)
        # Pin(9).irq(trigger=Pin.IRQ_FALLING, handler=scan)

        # Configure sensors
        # taps = EspKw.get_taps()
        # tap_sensors = {1: 19, 2: 22, 3: 28}
        # if taps[1]['sensor_status'] == 1:
        #     t1_sensor = Pin(tap_sensors[1], Pin.IN)
        #     t1_sensor.irq(trigger=Pin.IRQ_RISING |
        #                   Pin.IRQ_FALLING, handler=tap_pouring)
        #     enabled_taps += 1

        # if taps[2]['sensor_status'] == 1:
        #     t2_sensor = Pin(tap_sensors[2], Pin.IN)
        #     t2_sensor.irq(trigger=Pin.IRQ_RISING |
        #                   Pin.IRQ_FALLING, handler=tap_pouring)
        #     enabled_taps += 1

        # if taps[3]['sensor_status'] == 1:
        #     t3_sensor = Pin(tap_sensors[3], Pin.IN)
        #     t3_sensor.irq(trigger=Pin.IRQ_RISING |
        #                   Pin.IRQ_FALLING, handler=tap_pouring)
        #     enabled_taps += 1

        # Try to set the time
        try:
            set_time()
        except:
            pass

        # If data platform enabled, read data via API
        # if int(api_settings['status']) == 1:
        #     read_api()

    # System is ready, turn on the LED
    # Pin("LED", Pin.OUT).on()
    # display_default()

    # Start the web server
    web_server.run()

    # ========================== #
