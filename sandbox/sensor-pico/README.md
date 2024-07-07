# README

## Getting Started

This repository is intended to run on the Raspberry Pi Pico W. While it _is_ MicroPython and _should_ run on other microcontrollers (looking at you ESP), some modifications may need to be made. 

The two LCD Python files (api and i2c) are *required* for the chosen LCD controller (maintain the directory structure).

You must install the _micropython-phew_ package (use Thonny, connect to Pico, and use built in package manager)

The following items are *hard-coded* and will need to be modified to run:

- I2C port for the LCD
- UART port for the barcode scanner
- Pins for the hall-effect sensors



## Hardware List

| **Component**      | **Model**                    | **Hard-Coded Pin**      |
|--------------------|------------------------------|-------------------------|
| Microcontroller    | Raspberry Pi Pico W (RP2040) | N/A                     |
| Hall-Effect Sensor | HiLetgo 3144E A3144          | **T1:** _19_ **T2:** _22_ **T3:** _28_    |
| 16x2 LCD           | HiLetgo HD44780 IIC I2C1602  | I2C 0 _SDA (0)_ / _SCL (1)_ |
| QR/Barcode Scanner | GM67                         | UART 1 _Tx (8)_ / _Rx (9)_  |


