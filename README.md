# KegWatch
### Overview
KegWatch is a sensor designed to estimate how much beer is left in the kegs of your home kegerator. The code in this repository is intended to be used on custom designed hardware. KegWatch is unique as it is the only solution that can measure your beer without installing electronics inside the kegerator. The hardware is passive and won't require any modifications to beer lines, kegs, etc.

Using linear hall sensors and magnets I am able to measure how far the tap handle is from the beer tower. How does this help? We can use the tap handle position to calculate how much beer is being poured based on flow rate. Draft beer setups are (generally) closed systems with a constant pressure applied. Beer is drawn from the bottom of a keg and all of the empty space is replaced with CO2. In theory, the flow rate should remain the same from the first beer to the last! 

Disclaimer: Is this perfect? Absolutely not, but is it close enough...yup! In testing I have been able to get fairly accurate results. For example, the last two kegs I tested with were only off by about 6oz (each keg was 672oz and by the time they kicked KegWatch reported about 6oz remaining). There are a few things done to improve accuracy such as calibration and a feature I am working on: adding a digital offset.

Check out the Wiki in this repository for detailed information on requirements, setup, and general usage!

### Connectivity
KegWatch will connect to your home WiFi network and you are able to communicate with it a few different ways:

- Mobile App (currently in development)
- API calls directly to the device (see documentation)
- MQTT (for use in something like Home Assistant)
- WatchMy.Beer data platform (custom platform for beer-analytics, more to come on that)



