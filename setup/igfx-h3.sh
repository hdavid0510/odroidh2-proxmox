#!/bin/bash
# confirmed working on PROXMOX 7.0-11 clean iso install

echo -e "\033[103m\033[30m\033[1m  ODROID H3(+) PROXMOX igpu passthrough setup  \033[0m"



echo -e "\n\033[93m\033[1mUpdating GRUB parameter\033[0m"

sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="quiet"/GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on video=efifb:off iommu=pt pcie_acs_override=downstream"/g' /etc/default/grub
update-grub


echo -e "\n\033[93m\033[1mUnloading Intel igpu modules\033[0m"

echo "# Unload Intel igpu modules" | tee -a /etc/modprobe.d/pve-blacklist.conf
echo "blacklist snd_hda_intel" | tee -a /etc/modprobe.d/pve-blacklist.conf
echo "blacklist snd_hda_codec_hdmi" | tee -a /etc/modprobe.d/pve-blacklist.conf
echo "blacklist i915" | tee -a /etc/modprobe.d/pve-blacklist.conf


echo -e "\n\033[93m\033[1mEnabling vfio modules\033[0m"

echo "# PCIe passthrough" | tee -a /etc/modules
echo "vfio" | tee -a /etc/modules
echo "vfio_iommu_type1" | tee -a /etc/modules
echo "vfio_pci" | tee -a /etc/modules
echo "vfio_virqfd" | tee -a /etc/modules


echo -e "\n\033[93m\033[1mAdding options for kvm module\033[0m"

echo "options kvm ignore_msrs=1" | tee -a /etc/modprobe.d/kvm.conf
echo "options kvm report_ignored_msrs=0" | tee -a /etc/modprobe.d/kvm.conf


echo -e "\n\033[93m\033[1mDisabling VGA output from igpu\033[0m"

echo "options vfio-pci ids=8086:4e71,8086:4dc8" | tee -a /etc/modprobe.d/vfio.conf


echo -e "\n\033[93m\033[1mUpdating GRUB config\033[0m"

update-grub


echo -e "\n\033[93m\033[1mUpdating initramfs\033[0m"

update-initramfs -u -k all


echo -e "\n\033[0;32m\xE2\x9C\x94\033[0m \033[92m\033[1mSETUP FINISHED\033[0m"
echo -e "Reboot required to apply changes.\n"
