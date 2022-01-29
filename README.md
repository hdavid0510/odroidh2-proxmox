# ODROID H2 Proxmox Setup

Automated PROXMOX initial setup.


## 1. Download

Simply run as **root**:
```bash
cd ~/ && apt update && apt install git -y && git clone https://github.com/hdavid0510/proxmox-odroidh2 && cd proxmox-odroidh2 && chmod +x *.sh
```


## 2. Initial setup

### Usage

Simply run as **root**:
``` bash
./setup.sh
```

### How it works

* `setup.sh`
	1. Disable enterprise repository, enable no-subscription repository. Then update APT repository.  
	*Since knowing what package will be upgraded is important, package upgrade(`apt dist-upgrade`) should be done via web console manually.*
	2. Deploy byobu environment.  
	*If byobu environment is unnecessary, comment out `byobu-enable` in `./setup.sh` before running the script.*
	3. Run the following scripts.

* `suppress-subs.sh`
	1. Disable **No valid sub...** alert messages by editing `/usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js`.
	*Code source: https://johnscs.com/remove-proxmox51-subscription-notice/*
	2. Restart web server service.
	*Webpage must be refreshed manually to take effect.*

* `igfx.sh`
	1. Update GRUB kernel parameter.
	2. Blacklist/load kernel modules related to intel internal graphics.  
	*ODROID H2/H2+ uses Intel UHD Graphics 600 inside Intel Celeron J4105/J4115. Device ID of it has been hardcoded in the script. When using this script on other than ODROID H2, make sure to check device ID is correct.*
	3. Install kernel 5.11 and set to default booting kernel.
	*As of now, both `pve-kernel-5.13` and `pve-kernel-5.15` do not work well with iGPU passthrough. Thus `pve-kernel-5.11` is required. As PROXMOX `7.1-x` uses kernel `5.13` by default, it has to be manually installed and configured.
	4. Rebuild kernel.
	*System must be rebooted to take effect.*  
	Note: **In order to use iGPU passthrough, use version pinning below.**
