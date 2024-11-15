#!/usr/bin/env bash



readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# SHELL_FW=${SCRIPT_DIR}/submodules/dterletskiy/shell_fw/
SHELL_FW=${SCRIPT_DIR}/../sfw/
source ${SHELL_FW}/constants/console.sh
source ${SHELL_FW}/constants/constants.sh
source ${SHELL_FW}/base.sh
source ${SHELL_FW}/print.sh

readonly TEST=1



clear



ROOT_DIR=/mnt/dev/docker/builder/

QEMU_DIR=${ROOT_DIR}/qemu/master/x64/install/usr/local/
QEMU_ARM64=${QEMU_DIR}/bin/qemu-system-aarch64
QEMU_BRIDGE_HELPER=${QEMU_DIR}/libexec/qemu-bridge-helper
QEMU_DT=${ROOT_DIR}/#_workspace_#/qemu
QEMU_DTB=${QEMU_DT}.dtb
QEMU_DTS=${QEMU_DT}.dts
QEMU_DTB_RECOMPILE=${QEMU_DT}_recompile.dtb

QEMU_EFI_DIR=${ROOT_DIR}/tianocore/edk2/master/Build/ArmVirtQemu-AARCH64/DEBUG_GCC5/FV/
QEMU_EFI_ARM64=${QEMU_EFI_DIR}/QEMU_EFI-pflash.raw
QEMU_VARS_ARM64=${QEMU_EFI_DIR}/QEMU_VARS-pflash.raw
QEMU_PARAMETERS_EFI_EXEC+=" -drive if=pflash,format=raw,readonly=on,file=${QEMU_EFI_ARM64},size=64M"
QEMU_PARAMETERS_EFI_VARS+=" -drive if=pflash,format=raw,file=${QEMU_VARS_ARM64},size=64M"
QEMU_PARAMETERS_EFI=${QEMU_PARAMETERS_EFI_EXEC}
QEMU_PARAMETERS_EFI+=${QEMU_PARAMETERS_EFI_VARS}

UBOOT_DIR=${ROOT_DIR}/u-boot/2024.10/aarch64/install/
UBOOT=${UBOOT_DIR}/u-boot.bin

KERNEL=${ROOT_DIR}/images/artifacts/xen/dom0/kernel
KERNEL_CMD_LINE="root=/dev/vda verbose loglevel=7 console=hvc0 earlyprintk=xen"

INITRD=${ROOT_DIR}/images/artifacts/xen/dom0/rootfs.cpio.gz
ROOTFS=${ROOT_DIR}/images/artifacts/xen/dom0/rootfs.ext4

XEN_DIR=${ROOT_DIR}/yocto/dom0/product/tmp/deploy/images/qemuarm64/
XEN=${XEN_DIR}/xen-qemuarm64
XEN_EFI=${XEN_DIR}/xen-qemuarm64.efi
XEN_CMD_LINE="dom0_mem=3G,max:3G loglvl=all guest_loglvl=all console=dtuart pci-passthrough=yes"

DOM0_DIR=${ROOT_DIR}/yocto/dom0/product/tmp/deploy/images/qemuarm64/
DOM0_KERNEL=${DOM0_DIR}/Image
DOM0_KERNEL_CMD_LINE="root=/dev/ram verbose loglevel=7 console=hvc0 earlyprintk=xen"
DOM0_ROOTFS=${DOM0_DIR}/xen-image-minimal-qemuarm64.rootfs.ext4
DOM0_INITRD=${DOM0_DIR}/xen-image-minimal-qemuarm64.rootfs.cpio.gz

DOMD_DIR=${ROOT_DIR}/yocto/domd/product/tmp/deploy/images/qemuarm64/
DOMD_KERNEL=${DOMD_DIR}/Image
DOMD_KERNEL_CMD_LINE="root=/dev/vda verbose loglevel=7 console=hvc0 earlyprintk=xen"
DOMD_ROOTFS=${DOMD_DIR}/xen-guest-image-minimal-qemuarm64.rootfs.ext4
DOMD_INITRD=${DOMD_DIR}/xen-guest-image-minimal-qemuarm64.rootfs.cpio.gz

DRIVE_MAIN=${ROOT_DIR}/images/drive/install/main.img



function qemu_run_help( )
{
   ${QEMU_ARM64} -machine virt -machine help
   ${QEMU_ARM64} -machine help
   ${QEMU_ARM64} -device help
}

function qemu_run_01( )
{
   QEMU_PARAMETERS=""
   QEMU_PARAMETERS+=" -machine type=virt"
   QEMU_PARAMETERS+=" -machine virtualization=true"
   # QEMU_PARAMETERS+=" -enable-kvm"
   # QEMU_PARAMETERS+=" -cpu cortex-a57"
   QEMU_PARAMETERS+=" -cpu max,sme=off"
   QEMU_PARAMETERS+=" -smp 4"
   QEMU_PARAMETERS+=" -m 4096"
   QEMU_PARAMETERS+=" -d guest_errors"
   QEMU_PARAMETERS+=" -nodefaults"
   QEMU_PARAMETERS+=" -nographic"
   QEMU_PARAMETERS+=" -no-reboot"
   QEMU_PARAMETERS+=" -serial mon:stdio"
   # QEMU_PARAMETERS+=" -serial stdio"
   # QEMU_PARAMETERS+=" -chardev socket,id=qemu-monitor,host=localhost,port=7777,server=on,wait=off,telnet=on"
   # QEMU_PARAMETERS+=" -mon qemu-monitor,mode=readline"
   # QEMU_PARAMETERS+=" -mon qemu-monitor,mode=readline"
   # QEMU_PARAMETERS+=" -bios ${UBOOT}"
   QEMU_PARAMETERS+=" -drive if=none,index=0,id=main,file=${DRIVE_MAIN}"
   QEMU_PARAMETERS+=" -device virtio-blk-pci,modern-pio-notify=on,drive=main"
   QEMU_PARAMETERS+=" ${QEMU_PARAMETERS_EFI}"

   echo ----------------------------------------------------------------------------------------------------
   echo ${QEMU_ARM64} "${QEMU_PARAMETERS}"
   echo ----------------------------------------------------------------------------------------------------
   ${QEMU_ARM64} ${QEMU_PARAMETERS}
}



function qemu_run_02( )
{
   MACHINE=""
   MACHINE+=" -machine virt,acpi=off,secure=off,mte=on,virtualization=on,iommu=smmuv3,gic-version=max"
   MACHINE+=" -cpu max,sme=off"
   MACHINE+=" -smp 4"
   MACHINE+=" -m 8G"
   MACHINE+=" -d guest_errors"
   MACHINE+=" -nodefaults"
   MACHINE+=" -no-reboot"

   KERNEL=" -kernel ${XEN}"
   APPEND=" -append \"${XEN_CMD_LINE}\""

   GUEST_LOADER_DOM0_KERNEL=" \
      -device guest-loader,addr=0x60000000,kernel=${DOM0_KERNEL},bootargs=\"${DOM0_KERNEL_CMD_LINE}\" \
   "
   GUEST_LOADER_DOM0_INITRD=" \
      -device guest-loader,addr=0x52000000,initrd=${DOM0_INITRD} \
   "
   INITRD=" -initrd ${DOM0_INITRD}"

   SERIAL=" -serial mon:stdio"

   GRAPHIC=" -nographic"

   PCI_BRIDGE=" -device pci-bridge,id=bridge0,chassis_nr=1"

   DRIVE_DOM0_ROOTFS=" -drive if=none,index=0,id=rootfs_dom0,file=${DOM0_ROOTFS}"
   DRIVE_DOM0_ROOTFS+=" -device virtio-blk-pci,modern-pio-notify=off,drive=rootfs_dom0,bus=bridge0,addr=0x1"
   # DRIVE_DOM0_ROOTFS+=" -device virtio-blk-device,drive=rootfs_dom0"

   DRIVE_DOMD_ROOTFS=" -drive if=none,index=1,id=rootfs_domd,file=${DOMD_ROOTFS}"
   DRIVE_DOMD_ROOTFS+=" -device virtio-blk-pci,modern-pio-notify=off,drive=rootfs_domd,bus=bridge0,addr=0x2"
   # DRIVE_DOMD_ROOTFS+=" -device virtio-blk-device,drive=rootfs_domd"

   DRIVE_MAIN=" -drive if=none,index=2,id=main,file=${DRIVE_MAIN}"
   DRIVE_MAIN+=" -device virtio-blk-pci,modern-pio-notify=off,drive=main,bus=bridge0,addr=0x3"
   # DRIVE_MAIN+=" -device virtio-blk-device,drive=main"

   NETWORK_NETDEV_USER=" \
      -netdev user,id=eth0_inet,hostfwd=tcp::5550-:5555,ipv6=off \
      -device virtio-net-pci,netdev=eth0_inet,id=android \
   "

   NETWORK_NETDEV_BRIDGE=" \
      -netdev bridge,id=eth0_inet,br=virbr0,helper=${QEMU_BRIDGE_HELPER} \
      -device virtio-net-pci,netdev=eth0_inet,id=android \
   "

   NETWORK_NETDEV_TAP=" \
      -netdev tap,id=eth0_inet,ifname=ethernet_tap,script=no,downscript=no,vhost=on \
      -device virtio-net-pci-non-transitional,netdev=eth0_inet,id=android \
   "

   DEVICE_NET=${NETWORK_NETDEV_USER}

   COMMAND="${QEMU_ARM64}"
   COMMAND+=" ${MACHINE}"
   COMMAND+=" ${KERNEL}"
   COMMAND+=" ${APPEND}"
   # COMMAND+=" ${INITRD}"
   COMMAND+=" ${GUEST_LOADER_DOM0_KERNEL}"
   COMMAND+=" ${GUEST_LOADER_DOM0_INITRD}"
   COMMAND+=" ${SERIAL}"
   COMMAND+=" ${PCI_BRIDGE}"
   COMMAND+=" ${DRIVE_DOM0_ROOTFS}"
   COMMAND+=" ${DRIVE_DOMD_ROOTFS}"
   COMMAND+=" ${DRIVE_MAIN}"
   COMMAND+=" ${DEVICE_NET}"

   echo "${COMMAND}"
}

function print_setenv_var_size( )
{
   local VAR_NAME=${1}
   declare -n VAR_VALUE=${1}

   SIZE=$(stat -L -c%s "${VAR_VALUE}")
   # printf "${VAR_NAME}_SIZE': %d / 0x%x\n" "${SIZE}" "${SIZE}"
   # printf "setenv ${VAR_NAME}_SIZE 0x%x\n" "${SIZE}"
   printf "%-35s 0x%x\n" "setenv ${VAR_NAME}_SIZE" "${SIZE}"
}

function print_setenv_var_address( )
{
   local VAR_NAME=${1}
   declare -n VAR_VALUE=${1}

   printf "%-35s 0x%x\n" "setenv ${VAR_NAME}" "${VAR_VALUE}"
}

function print_setenv_var_value( )
{
   local VAR_NAME=${1}
   declare -n VAR_VALUE=${1}

   printf "%-35s \"%s\"\n" "setenv ${VAR_NAME}" "${VAR_VALUE}"
}

function qemu_run_03( )
{
   DTB=${QEMU_DTB}
   ROOTFS=${ROOT_DIR}/yocto/product/tmp/deploy/images/rootfs_domd.ext4
   UBOOT=${ROOT_DIR}/#_workspace_#/u-boot/2024.10/aarch64/u-boot.bin
   KERNEL=${ROOT_DIR}/yocto/product/tmp/deploy/images/Image
   KERNEL_DOM0=${KERNEL}
   KERNEL_DOMU=${KERNEL}

   XEN_ADDRESS=0x50000000
   DTB_ADDRESS=0x51000000
   ROOTFS_ADDRESS=0x52000000
   KERNEL_DOM0_ADDRESS=0x60000000
   KERNEL_DOMU_ADDRESS=0x65000000

   BOOTARGS_XEN="dom0_mem=256M loglvl=info"
   BOOTARGS_DOM0="earlyprintk=serial,ttyAMA0 console=hvc0 earlycon=xenboot clk_ignore_unused rw root=/dev/ram0"
   BOOTARGS_DOMU="rw root=/dev/ram0 console=ttyAMA0"

   echo "-------------------------------------------------------------------------------------------------"
   print_setenv_var_address XEN_ADDRESS
   print_setenv_var_address DTB_ADDRESS
   print_setenv_var_address ROOTFS_ADDRESS
   print_setenv_var_address KERNEL_DOM0_ADDRESS
   print_setenv_var_address KERNEL_DOMU_ADDRESS

   printf "\n"

   print_setenv_var_size XEN
   print_setenv_var_size DTB
   print_setenv_var_size ROOTFS
   print_setenv_var_size KERNEL_DOM0
   print_setenv_var_size KERNEL_DOMU

   printf "\n"

   print_setenv_var_value BOOTARGS_XEN
   print_setenv_var_value BOOTARGS_DOM0
   print_setenv_var_value BOOTARGS_DOMU

   echo "-------------------------------------------------------------------------------------------------"

   QEMU_PARAMETERS=""
   QEMU_PARAMETERS+=" -machine virt-8.0,acpi=off,secure=off,mte=off,virtualization=on"
   QEMU_PARAMETERS+=" -cpu max,sme=off"
   QEMU_PARAMETERS+=" -smp 4"
   QEMU_PARAMETERS+=" -m 8G"
   QEMU_PARAMETERS+=" -d guest_errors"
   QEMU_PARAMETERS+=" -nographic"
   QEMU_PARAMETERS+=" -no-reboot"
   QEMU_PARAMETERS+=" -bios ${UBOOT}"
   QEMU_PARAMETERS+=" -device loader,file=${XEN},force-raw=on,addr=${XEN_ADDRESS}"
   QEMU_PARAMETERS+=" -device loader,file=${DTB},addr=${DTB_ADDRESS}"
   QEMU_PARAMETERS+=" -device loader,file=${INITRD},addr=${ROOTFS_ADDRESS}"
   QEMU_PARAMETERS+=" -device loader,file=${KERNEL_DOM0},addr=${KERNEL_DOM0_ADDRESS}"
   QEMU_PARAMETERS+=" -device loader,file=${KERNEL_DOMU},addr=${KERNEL_DOMU_ADDRESS}"

   COMMAND="${QEMU_ARM64} ${QEMU_PARAMETERS}"
   echo ----------------------------------------------------------------------------------------------------
   echo "${COMMAND}"
   echo ----------------------------------------------------------------------------------------------------
   eval "${COMMAND}"
}

function compile_dt( )
{
   local IN_DTS=${1}
   local OUT_DTB=${2}

   local COMMAND="dtc -I dts -O dtb -o ${OUT_DTB} ${IN_DTS}"
   print_ok ${COMMAND}
   eval "${COMMAND}"
}

function decompile_dt( )
{
   local IN_DTB=${1}
   local OUT_DTS=${2}

   local COMMAND="dtc -I dtb -O dts -o ${OUT_DTS} ${IN_DTB}"
   print_ok ${COMMAND}
   eval "${COMMAND}"

}



LD_LIBRARY_PATH_QEMU="${QEMU_DIR}/lib/"
LD_LIBRARY_PATH_QEMU+=":${QEMU_DIR}/lib/x86_64-linux-gnu/"
COMMAND="export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LD_LIBRARY_PATH_QEMU}"
print_ok "${COMMAND}"
eval "${COMMAND}"



COMMAND=$( qemu_run_02 )

print_ok "${COMMAND} -machine dumpdtb=${QEMU_DTB}"
eval "${COMMAND} -machine dumpdtb=${QEMU_DTB}"

decompile_dt ${QEMU_DTB} ${QEMU_DTS}
compile_dt ${QEMU_DTS} ${QEMU_DTB_RECOMPILE}

print_ok "${COMMAND}"
eval "${COMMAND}"
