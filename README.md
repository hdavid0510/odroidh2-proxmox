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


## 3. PROXMOX version pin


### Usage

Simply run as **root**:
```bash
./proxmox-version-pin.sh
```

### Why?

In order to use iGPU passthrough, kernel and hypervisor should support it. BUT, it seems it works well only until PROXMOX `7.0-x`; it somehow failes to launch VMs with iGPU passthrough-ed with `error 1`. To resolve this, I had to **downgrade** PROXMOX from `7.1-x` to `7.0-x`. Downgrading system caused some stability issue, so I ended up installing PROXMOX all over again.  
When updating/upgrading packages via PROXMOX web console and APT in PROXMOX `7.0-x` environment, it will be directly upgraded to PROXMOX `7.1-x`. To prevent this, I pinned PROXMOX packages in `7.0-x` version.

**DISCLAIMER: Normally, PROXMOX should run the lastest version. This is for test use only. USE THE VERSION PINNING IN YOUR OWN RISK.**

### Packages affected

I am not sure which package does which, so I found some packages to pin through some trial-and-errors. **Some required packages may have been missed in this list; some packages may have to be removed.** I'll update those when error happens - *yes, that trial-and-error method is still on-going*.  
It is seemed to be QEMU-related problem, but PROXMOX version seems to be dependent to the QEMU version. Possibility for using latest PROXMOX with pinned(older) QEMU package is under investigation.

| Package | Latest | Pinned | Pin Required? |
| ------- | ------ | ------- | ------------- |
| proxmox-ve | 7.1-1 | 7.0-2 | **REQUIRED** * |
| pve-kernel-helper | 7.1-8 | 7.0-7 | Not Required |
| pve-manager | 7.1-10 | 7.0-15 | Not Required ** |
| pve-qemu-kvm | 6.1.0-2 | 6.0.0-4 | Not Required |
| qemu-server | 7.1-4 | 7.0-19 | Not Required |

check version installed with:
```bash
apt list --installed proxmox-ve pve-kernel-helper pve-manager pve-qemu-kvm qemu-server
```

 *Upgrading `proxmox-ve` causes linux kernel 5.13 installed, make PCIe passthrough no longer available. Installing linux kernel 5.15 also not working.  
 **`pve-manager` version is printed on the webpage proxmox version info. In order to match the version of `proxmox-ve` and the displayed one, pinning `pve-manager` is considered to be *semi-required*.