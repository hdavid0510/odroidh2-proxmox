#!/bin/bash

echo -e "\n\033[103m\033[30m\033[1m  ODROID H2 PROXMOX i2c-oled monitoring service  \033[0m"


# echo -e "\n\033[93m\033[1mSettings\033[0m"

# TODO: automatically detect I2C device no. and port
I2C_PORT=2

# TODO: set orientation.
ORIENTATION=0	# 0 deg
#ORIENTATION=1	# 90 deg clockwise
#ORIENTATION=2	# 180 deg
#ORIENTATION=3	# 270 deg clockwise


echo -e "\n\033[93m\033[1mInstalling prerequisities\033[0m"

apt -yqq update
apt -yqq install python3 python3-pip python3-smbus python3-psutil python3-pil fonts-dejavu-core fonts-noto-mono
pip install -U pip
pip install -U luma.core


echo -e "\n\033[93m\033[1mInstalling service\033[0m"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
mkdir -p /opt/sysmon-oled
cp -r ${SCRIPT_DIR}/../sysmon-oled /opt/sysmon-oled
cp ${SCRIPT_DIR}/sysmon-oled.service /etc/systemd/system/sysmon-oled.service
sed -i 's/%I2CPORT%/'${I2C_PORT}'/g' /etc/systemd/system/sysmon-oled.service
sed -i 's/%ORIENTATION%/'${ORIENTATION}'/g' /etc/systemd/system/sysmon-oled.service
systemctl daemon-reload
systemctl enable sysmon-oled.service


echo -e "\n\033[0;32m\xE2\x9C\x94\033[0m \033[92m\033[1mSETUP FINISHED\033[0m"
echo -e "I2C OLED system monitoring service will automatically be started on boot from now on.\n"