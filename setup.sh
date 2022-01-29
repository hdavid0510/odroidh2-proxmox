#!/bin/bash

echo -e "\033[103m\033[30m\033[1m  ODROID H2 PROXMOX initial setup  \033[0m"


echo -e "\n\033[93m\033[1mEdit APT repository\033[0m"

sed -i 's|deb https://enterprise.proxmox.com/debian/pve bullseye pve-enterprise|# deb https://enterprise.proxmox.com/debian/pve bullseye pve-enterprise|g' /etc/apt/sources.list.d/pve-enterprise.list
echo -e "deb http://download.proxmox.com/debian/pve bullseye pve-no-subscription" | tee /etc/apt/sources.list.d/pve-no-subscription.list
apt update


echo -e "\n\033[93m\033[1mInstall byobu\033[0m"

tar -xzf byobu.tar.gz --directory ~/
apt install byobu -y
byobu-enable


[ -f ./supporess-subs.sh ] && chmod +x ./supporess-subs.sh && ./supporess-subs.sh
[ -f ./igfx.sh ] && chmod +x ./igfx.sh && ./igfx.sh


echo -e "\n\033[0;32m\xE2\x9C\x94\033[0m \033[92m\033[1mPROXMOX INIT SETUP FINISHED\033[0m"