#!/bin/bash

echo -e "\n\033[103m\033[30m\033[1m  ODROID H2 PROXMOX i2c-oled monitoring service  \033[0m"


# echo -e "\n\033[93m\033[1mSettings\033[0m"

echo -e "\n\033[93m\033[1mInstalling prerequisities\033[0m"

apt -yqq update
apt -yqq install python3 python3-pip python3-smbus python3-psutil python3-pil fonts-dejavu-core fonts-noto-mono
python3 -m pip install -U pip
python3 -m pip install -U luma.core luma.oled


echo -e "\n\033[93m\033[1mInstalling service\033[0m"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
mkdir -p /opt/sysmon-oled
cp -r ${SCRIPT_DIR}/../sysmon-oled /opt/
cp ${SCRIPT_DIR}/sysmon-oled.service /etc/systemd/system/sysmon-oled.service
systemctl daemon-reload
systemctl enable sysmon-oled.service


echo -e "\n\033[0;32m\xE2\x9C\x94\033[0m \033[92m\033[1mSETUP FINISHED\033[0m"
echo -e "I2C OLED system monitoring service will automatically be started on boot from now on.\n"
