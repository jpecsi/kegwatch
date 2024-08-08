## Overview
What is KegWatch? KegWatch is a device I designed and built to monitor my kegerator and estimate how much beer is left in the kegs! Having a kegerator at home is a lot of fun and it works great since we love to host friends/family, but one of my issues was not being able to see how much beer we had left. Surprisingly, there were very few options available geared toward home users vs commercial bars. The only slightly promising solution was a product that was sold as a smart keg scale but it had so many downsides like cost (had to buy one per keg and mine is a two tap kegerator) and size (too tall for my kegerator). I even explored a few commercial options that used flow rate sensors in the beer lines, but they got crazy expensive and were not as open for development. Truthfully, I also didn't like the idea of putting electronics inside the kegerator or messing with my beer lines. The logical next step was to just build my own!

KegWatch is a unique approach to this problem because it is non-invasive. No electronics inside the kegerator and nothing that sits in the beer lines. You can use KegWatch without making any modifications to your home system! The device sits on top of the tower and uses linear hall sensors to monitor the tap handles and measure how far away they are from the unit. Draft beer setups are closed systems with constant pressure; beer is drawn from the bottom of a keg and all of the empty space is replaced with CO2. In theory, the flow rate should remain the same from the first beer to the last! Using time to calculate flow rate is **not** 100% accurate, but it is most definitely close enough (especially for home use). I'm continuing to make adjustments/improvements for accuracy but in recent tests with a 672oz keg, when it kicked I was only off by a total of 6oz.

[You can read more about the project here](https://joepecsi.com/projects/kegwatch) on my personal website. I plan to keep everything open source, so this repo will house the sensor code, schematics for the hardware, as well as code/packages for the server side functionality.


## Platform
### KegWatch
KegWatch refers to the physical device and the software it runs, this is the core product that provides basic functionality like measuring beer poured and reporting how much beer is remaining. KegWatch connects to your home network via Wi-Fi and provides physical feedback through LED indicators to report how full the kegs are, and can also report over MQTT to a platform such as Home Assistant.

I am currently testing an on-device web interface as well as a mobile app to improve the interaction experience.


### WatchMy.Beer
WatchMy.Beer is a data platform that expands the capabilities of KegWatch. You can self host the platform (via Docker) which consists of a server, database, visualization interface, and administration interface. The platform allows for increased data collection which provides awesome beer focused analytics! Here is an example of data you can collect/visualize:

* How much beer is remaining across all of your taps
* Beer history (what's been on tap before, how long they took to consume)
* Beer popularity (based on average time to consume a specific beer)
* A log of all pours based on beer, tap, or person
* Scoreboard/leaderboard of who consumed the most beer
* View consumption data at a specific date/time range (want to see who dran the most at Thanksgiving?)


## Hardware
KegWatch is a custom designed device based on the ESP32 microcontroller and uses SS49E linear hall sensors (one per tap). For added fun, a GM67 QR Code scanner is added on for tagging beer to people.

I am working on the next iteration of hardware, and will share schematics once tested and working.





