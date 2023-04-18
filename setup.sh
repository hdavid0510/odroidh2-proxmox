#!/bin/bash

echo -e "\033[103m\033[30m\033[1m  ODROID H2/H3 PROXMOX initial setup  \033[0m"

# Check if board is H2/H3
BOARD=$(dmidecode | grep ODROID | head -n 1 | awk '{print $3}')
if [ "${BOARD}" == "ODROID-H2" ] || [ "${BOARD}" == "ODROID-H3" ]; then
	echo ${BOARD} "detected!"
else
	echo -e "\n\033[93m\033[1mODROID H2/H3 not detected.\033[0m"
	exit
fi


echo -e "\n\033[93m\033[1mEdit APT repository\033[0m"

sed -i 's|deb https://enterprise.proxmox.com/debian/pve bullseye pve-enterprise|# deb https://enterprise.proxmox.com/debian/pve bullseye pve-enterprise|g' /etc/apt/sources.list.d/pve-enterprise.list
echo -e "deb http://download.proxmox.com/debian/pve bullseye pve-no-subscription" | tee /etc/apt/sources.list.d/pve-no-subscription.list
apt update


echo -e "\n\033[93m\033[1mInstall byobu\033[0m"

tar -xzf byobu.tar.gz --directory ~/
apt install byobu -y
byobu-enable


# PROXMOX subscription notice suppress
[ -f ./setup/supporess-subs.sh ] && chmod +x ./setup/supporess-subs.sh && ./setup/supporess-subs.sh


# OLED system monitor
[ -f ./setup/sysmon-oled.sh ] && chmod +x ./setup/sysmon-oled.sh && ./setup/sysmon-oled.sh


# iGPU passthrough based on board type
if [ "${BOARD}" == "ODROID-H2" ]; then
	[ -f ./setup/igfx-h2.sh ] && chmod +x ./setup/igfx-h2.sh && ./setup/igfx-h2.sh
elif [ "${BOARD}" == "ODROID-H3" ]; then
	[ -f ./setup/igfx-h3.sh ] && chmod +x ./setup/igfx-h3.sh && ./setup/igfx-h3.sh
fi


echo -e "\n\033[0;32m\xE2\x9C\x94\033[0m \033[92m\033[1mPROXMOX INIT SETUP FINISHED\033[0m"
