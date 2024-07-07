#!/bin/bash

echo "alias kw-sensor='sudo /opt/kegwatch/sensor/sensor.py &'" >> ~/.bashrc
echo "alias kw-sensor-f='sudo /opt/kegwatch/sensor/sensor.py'" >> ~/.bashrc
echo "alias kw-cal='/opt/kegwatch/sensor/util/calibrate.py'" >> ~/.bashrc
echo "alias kw-keg='/opt/kegwatch/sensor/util/add_keg.py'" >> ~/.bashrc
echo "alias kw-swtst='/opt/kegwatch/sensor/util/switch_test.py'" >> ~/.bashrc
echo "alias kw-users='/opt/kegwatch/sensor/util/users.py'" >> ~/.bashrc
echo "alias kw-scan='/opt/kegwatch/sensor/util/scanner_check.py'" >> ~/.bashrc
echo "alias kw-help='/opt/kegwatch/sensor/util/help.py'" >> ~/.bashrc
echo "alias kw-clean='/opt/kegwatch/sensor/util/cleanup.py'" >> ~/.bashrc



