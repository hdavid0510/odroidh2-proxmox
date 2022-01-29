# ODROID H2 Proxmox Setup

Automated PROXMOX initial setup.

## Usage

Simply run as **root**:
``` bash
(cd ~/ && apt update && apt install git -y && git clone https://github.com/hdavid0510/odroidh2-proxmox && cd odroidh2-proxmox && chmod +x setup.sh && ./setup.sh )
```

## How it works

### setup.sh
1. Disable enterprise repository, enable no-subscription repository. Then update APT repository.  
*Since knowing what package will be upgraded is important, package upgrade(`apt full-upgrade`) should be done via web console manually.*
2. Deploy byobu environment.  
*If byobu environment is unnecessary, comment out `byobu-enable` in `./setup.sh` before running the script.*
3. Run the following scripts.

### suppress-subs.sh
1. Disable **No valid sub...** alert messages by editing `/usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js`.
*Code source: https://johnscs.com/remove-proxmox51-subscription-notice/*
2. Restart web server service.
*Webpage must be refreshed manually to take effect.*

### igfx.sh
1. Update GRUB kernel parameter.
2. Blacklist/load kernel modules related to intel internal graphics.  
*ODROID H2/H2+ uses Intel UHD Graphics 600 inside Intel Celeron J4105/J4115. Device ID of it has been hardcoded in the script. When using this script on other than ODROID H2, make sure to check device ID is correct.*
3. Rebuild kernel.
*System must be rebooted to take effect.*
