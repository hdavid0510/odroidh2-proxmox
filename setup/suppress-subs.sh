#!/bin/bash

echo -e "\n\033[103m\033[30m\033[1m  ODROID H2 PROXMOX igpu passthrough setup  \033[0m"
echo -e "  source: https://johnscs.com/remove-proxmox51-subscription-notice/"


echo -e "\n\033[93m\033[1mUpdating PROXMOX webpage script\033[0m"

sed -Ezi.bak "s/(Ext.Msg.show\(\{\s+title: gettext\('No valid sub)/void\(\{ \/\/\1/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js


echo -e "\n\033[93m\033[1mRestarting web service\033[0m"

systemctl restart pveproxy.service


echo -e "\n\033[0;32m\xE2\x9C\x94\033[0m \033[92m\033[1mSETUP FINISHED\033[0m"
echo -e "Message suppression will be available after refreshing the page.\n"