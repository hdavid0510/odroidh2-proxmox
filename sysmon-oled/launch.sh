#!/bin/bash

I2C_PORT=3c

ORIENTATION=0	# 0 deg
#ORIENTATION=1	# 90 deg clockwise
#ORIENTATION=2	# 180 deg
#ORIENTATION=3	# 270 deg clockwise

DISPLAY="ssd1306"
WIDTH=128
HEIGHT=32

for d in {0..4}; do
	if [ "$(i2cdetect -y -r $d | grep ${I2C_PORT})" != "" ]; then
		I2CPORT=$d
		break;
	fi
done

if [ -z "$I2CPORT" ]; then
	echo "No I2C OLED display device found"
	exit 1
fi

/opt/sysmon-oled/sys_info.py --i2c-port ${I2CPORT} --display ${DISPLAY} --width ${WIDTH} --height ${HEIGHT} --rotate ${ORIENTATION}
