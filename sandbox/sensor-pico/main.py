# ========== LIBRARIES ========== #
import json
import time
import network
import socket
import machine
import struct
import urequests
from machine import I2C, Pin, UART
from lcd.pico_i2c_lcd import I2cLcd
from phew import logging, server, connect_to_wifi, is_connected_to_wifi, access_point
from phew.template import render_template
import _thread

# =============================== #





# ========== CALIBRATION ========== #
def calibration_pour(t):
    global CAL_COUNT,CAL_MODE
    CAL_COUNT += 1
    
    if CAL_COUNT < CAL_POURS:
        CAL_RATES.append(t)
        lcd.clear()
        lcd.putstr(("Pour " + str(CAL_COUNT) + " of " + str(CAL_POURS)).center(16))
        lcd.putstr(("Complete!").center(16))
        
    else:
        CAL_RATES.append(t)
        CAL_MODE = False
        lcd.clear()
        lcd.putstr(("Pours Complete!").center(16))
        lcd.putstr(("See Web Portal").center(16))
    

def calibration_calc(p1,p2,p3,p4):
    global CAL_COUNT,CAL_POURED,CAL_TAP,CAL_RATES
    total_poured,flow_rate = 0,0
    poured,pour_count = 0,0
    
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
    for item in config[("tap_"+str(CAL_TAP))]:
        item['flow_rate'] = flow_rate
        item['remaining'] = beer_remaining

    with open('config.json', 'w') as f:
        json.dump(config, f)
        
    # Report externally if required
    if int(mqtt_settings['status']) == 1:
        push_mqtt()
    if int(api_settings['status']) == 1:
        push_api(CAL_TAP,poured,"Calibration")

    CAL_COUNT,CAL_POURED,CAL_TAP = 0,0,0
    CAL_RATES = []
    display_default()


def calibration_kickoff(t,n):
    global CAL_MODE,CAL_POURS,CAL_TAP
    CAL_MODE = True
    CAL_POURS = int(n)
    CAL_TAP = int(t)
    lcd.clear()
    lcd.putstr(("Calibrate Tap " + str(t)).center(16))
    lcd.putstr((str(n) + " Pours").center(16))
# ================================= #





# ========== WEB SERVER ========== #
def index(request):
    return render_template("html/index.html", title="KegWatch | Data by the Pint")

def configure_cal(request):
    print(request.method)
    if request.method == 'GET':
        return render_template("html/calibrate.html")
    if request.method == 'POST':    
        selected_tap = request.form.get("select_tap", None)
        select_numpours = request.form.get("select_numpours", None)
        p1 = request.form.get("p1_amount", None)

        if p1 == None:
            calibration_kickoff(selected_tap,select_numpours)
            return render_template("html/calibrate"+select_numpours+".html")
        else:
            calibration_calc(request.form.get("p1_amount", None),request.form.get("p2_amount", None),request.form.get("p3_amount", None),request.form.get("p4_amount", None))
            return render_template("html/default.html",content="Boom! System calibrated")

@server.catchall()
def my_catchall(request):
    return "No matching route", 404


# ================================= #





# ========== DISPLAY MGMT ========== #
# String formatter
def format_str(s):
    target_length = 16
    if len(s) > target_length:
        s = s[:target_length]
    elif len(s) < target_length:
        for x in range(target_length-len(s)):
            s += " "
    return s
    
# Default Display
def display_default():
    config = load_config()
    
    # Configure display based on # of taps
    if enabled_taps == 0:
        lcd.clear()
        lcd.putstr("No Taps".center(16))
        lcd.putstr("Configured!".center(16))
        
    elif enabled_taps == 1:
        lcd.clear()
        lcd.putstr("Tap 1 Remaining".center(16))
        lcd.putstr((str(round(taps[1]["remaining"],2)) + "oz").center(16))
        
    elif enabled_taps == 2:
        lcd.clear()
        lcd.putstr(format_str(("Tap 1: " + str(round(taps[1]["remaining"],2)) + "oz")))
        lcd.putstr(format_str(("Tap 2: " + str(round(taps[2]["remaining"],2)) + "oz")))
        
    elif enabled_taps == 3:
        lcd.clear()
        lcd.putstr(format_str("1:" + str(round(taps[1]["remaining"]+"oz")) + "3:" + str(round(taps[3]["remaining"]+"oz"))))
        lcd.putstr(format_str("2:" + str(round(taps[2]["remaining"]+"oz"))))
        
# Show pouring status    
def display_pouring(m,t,o):
    if m == 1:
        # Tap Open
        lcd.clear()
        if CAL_MODE:
            lcd.putstr(("Tap  " + str(t)).center(16))
            lcd.putstr("Calibration Pour")
        else:   
            if consumer == "Anonymous":
                lcd.putstr(("Tap  " + str(t)).center(16))
                lcd.putstr("Pouring...".center(16))
            else:
                lcd.putstr(("Tap " + str(t) + " Pouring").center(16))
                if len(consumer) > 16:
                    lcd.putstr(consumer.split(" ")[0].center(16))
                else:
                    lcd.putstr(consumer.center(16))
    
    elif m == 0:
        # Tap Closed
        lcd.clear()
        lcd.putstr("Pour Complete:".center(16))
        lcd.putstr((str(round(o,2)) + "oz").center(16))

    elif m == 3:
        # Tap Closed
        lcd.clear()
        lcd.putstr("Inactive Tap".center(16))
        lcd.putstr(("No Beer Logged!").center(16))

    
# ================================== #





# ========== NETWORK MGMT ========== #
# Create local/ad-hoc network for setup
def connect_network(w):
    def gen_ap():
        access_point("KegWatch",  password=None)
        lcd.clear()
        lcd.putstr("SSID: KegWatch")
        lcd.putstr("PASS: 1234567890")
        time.sleep(3)

    if w["status"] == 0:
        ip = gen_ap()
        
    elif w["status"] == 1:
        ip = connect_to_wifi(w["ssid"],w["password"])
        if is_connected_to_wifi():
            lcd.clear()
            lcd.putstr("Connected!".center(16))
            lcd.putstr(ip.center(16))
            time.sleep(3)
        else:
            gen_ap()

# Return current time as string
def get_time():
    t = time.localtime()
    return(str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + " " + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5]))

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
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

# ================================== #





# ========== FUNCTIONS ========== #
# Read JSON
def load_config():
    # Load configuration
    f = open("config.json","r")
    return json.load(f)


# Get input from barcode scanner
def scan(pin):
    if uart.any():
        b = uart.read()
    try:
        msg = b.decode('utf-8')
        global consumer
        consumer = msg[:-1]
    except:
        pass




# Tap Handler
def tap_pouring(pin):
    # Variables for timer
    global start
    global stop

    # Get Tap 
    #tap_id = list(tap_sensors.keys())[list(tap_sensors.values()).index(int((str(pin).split('('))[1][:2]))]
    if pin == t1_sensor:
        tap_id = 1
    elif pin == t2_sensor:
        tap_id = 2
    elif pin == t3_sensor:
        tap_id = 3
        
    if pin.value() == 1:
        # Tap is open - mark the time
        start = time.ticks_ms()
        display_pouring(1,tap_id,0)

    if pin.value() == 0:
        # Tap is closed - mark the time
        stop = time.ticks_ms()
        
        # Calculate time tap was open
        time_open = time.ticks_diff(stop,start)
        
        # Calculate beer poured
        if CAL_MODE:
            calibration_pour(time_open)
        else:
            calc_beer(tap_id,time_open)


# Calculate Beer Poured
def calc_beer(t,s):

    # Check to make sure the keg is active
    status = int(taps[t]["beer_status"])
    global consumer
    if status == 1:
        
        # Figure out beer poured/remaining
        beer_poured = (s * float(taps[t]["flow_rate"]))
        beer_remaining = (float(taps[t]["remaining"]) - beer_poured)
        display_pouring(0,t,beer_poured)

        # Don't let remaining go negative, negative beer is sad and impossible
        if beer_remaining <= 0:
            beer_remaining = 0
            status = 0

        # Update the config
        for item in config[("tap_"+str(t))]:
            item['remaining'] = beer_remaining

        with open('config.json', 'w') as f:
            json.dump(config, f)
        
        # Report externally if required
        if int(mqtt_settings['status']) == 1:
            push_mqtt()
        if int(api_settings['status']) == 1:
            push_api(t,beer_poured,consumer)
            
        # Reset the consumer
        consumer = "Anonymous"
            
        time.sleep(1)
        display_default()
    else:
        display_pouring(3,t,0)


def push_mqtt():
    pass

def push_api(t,p,c):
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
        lcd.putstr("API Error!".center(16))
        lcd.putstr("Saving Locally".center(16))
        time.sleep(2)
    
def read_api():
    try:
        response = urequests.get(api_host+"/kegs").json()
        for x in range(len(response)):
            if response[x]['status'] == 1:
                # Update the config
                for item in config[("tap_"+str(response[x]['tap']))]:
                    if item['keg_id'] == response[x]['id'] and item['remaining'] < response[x]['remaining']:
                        difference = response[x]['remaining'] - item['remaining']
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
       lcd.putstr("API Error!".center(16))
       lcd.putstr("Local Only".center(16))
       time.sleep(2)
    
# =============================== #





# ========== MAIN ========== #

# Setup display
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Set consumer
consumer = "Anonymous"

# Load configs
config = load_config()

# Tap configuration
enabled_taps = 0
taps = {
    1: config['tap_1'][0],
    2: config['tap_2'][0],
    3: config['tap_3'][0]
}

# System configuration
mqtt_settings = config['mqtt'][0]
api_settings = config['data_platform'][0]
wifi_settings = config['wifi'][0]
api_host = ("http://" + api_settings["host"] + ":" + api_settings["port"])

# Configure network
connect_network(wifi_settings)

# Calibration mode parameters
CAL_MODE = False
CAL_COUNT,CAL_POURS,CAL_TAP = 0,0,0
CAL_RATES = []


# Configure barcode scanner
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9),bits=8, parity=None, stop=1,txbuf=10,rxbuf=10)
Pin(9).irq(trigger=Pin.IRQ_FALLING, handler=scan)

# Configure sensors
tap_sensors = {1:19,2:22,3:28}
if taps[1]['sensor_status'] == 1:    
    t1_sensor = Pin(tap_sensors[1], Pin.IN)
    t1_sensor.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = tap_pouring)
    enabled_taps += 1

if taps[2]['sensor_status'] == 1:   
    t2_sensor = Pin(tap_sensors[2], Pin.IN)
    t2_sensor.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = tap_pouring)
    enabled_taps += 1

if taps[3]['sensor_status'] == 1:   
    t3_sensor = Pin(tap_sensors[3], Pin.IN)
    t3_sensor.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = tap_pouring)
    enabled_taps += 1
    
# Try to set the time
try:
    set_time()
except:
    pass

# If data platform enabled, read data via API
if int(api_settings['status']) == 1:
    read_api()


# System is ready, turn on the LED
Pin("LED", Pin.OUT).on()
display_default()


# Start the web server
server.add_route("/",index,methods=["GET"])
server.add_route("/calibrate", configure_cal,["POST",'GET'])
server.run()

# ========================== #








