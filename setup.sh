#!/bin/bash

echo -e "\033[103m\033[30m\033[1m  ODROID H2 PROXMOX initial setup  \033[0m"


echo -e "\n\033[93m\033[1mEdit APT repository\033[0m"

sed -i 's|deb https://enterprise.proxmox.com/debian/pve bullseye pve-enterprise|# deb https://enterprise.proxmox.com/debian/pve bullseye pve-enterprise|g' /etc/apt/sources.list.d/pve-enterprise.list
echo -e "deb http://download.proxmox.com/debian/pve bullseye pve-no-subscription" | tee -a /etc/apt/sources.list.d/pve-no-subscription.list
apt update


echo -e "\n\033[93m\033[1mInstall byobu\033[0m"

tar -xzf byobu-2.4.2.tar.gz --directory ~/
apt install byobu -y
byobu-enable
echo -e "byobu will be activated automatically in new shell instances from now on.\n"


[ -f ./supporess-subs.sh ] && ./supporess-subs.sh
[ -f ./igfx.sh ] && ./igfx.sh

echo -e "\n\033[0;32m\xE2\x9C\x94\033[0m \033[92m\033[1mPROXMOX INIT SETUP FINISHED\033[0m"