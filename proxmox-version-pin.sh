#!/bin/bash

echo -e "\033[103m\033[30m\033[1m  PROXMOX v7.0* pin  \033[0m"


echo -e "\n\033[93m\033[1mInstall Pin files\033[0m"
for f in preferences.d/*.pin; do
	cp $f /etc/apt/preferences.d/
done


echo -e "\n\033[93m\033[1mAPT repository update\033[0m"
apt update


echo -e "\n\033[0;32m\xE2\x9C\x94\033[0m \033[92m\033[1mPIN SETUP FINISHED\033[0m"