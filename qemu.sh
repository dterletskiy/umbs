#!/usr/bin/env bash



readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
readonly TIMESTAMP=$(date +'%Y.%m.%d_%H.%M.%S')

# SHELL_FW=${SCRIPT_DIR}/submodules/dterletskiy/shell_fw/
SHELL_FW=${SCRIPT_DIR}/../sfw/
source ${SHELL_FW}/constants/console.sh
source ${SHELL_FW}/constants/constants.sh
source ${SHELL_FW}/base.sh
source ${SHELL_FW}/print.sh



clear



ROOT_DIR=/mnt/dev/docker/builder/

DUMP_DIR=${ROOT_DIR}/#_workspace_#/dump/
QEMU_DUMP_DIR=${DUMP_DIR}/qemu/${TIMESTAMP}/
mkdir -p ${QEMU_DUMP_DIR}

QEMU_COMMAND_DUMP=${QEMU_DUMP_DIR}/command.txt
QEMU_DT_DUMP_DIR=${QEMU_DUMP_DIR}/dtb/
QEMU_DTB_DUMP=${QEMU_DT_DUMP_DIR}/original.dtb
QEMU_DTS_DUMP=${QEMU_DT_DUMP_DIR}/original.dts
QEMU_DTB_DUMP_RECOMPILE=${QEMU_DT_DUMP_DIR}/recompiled.dtb
QEMU_LOG_DUMP=${QEMU_DUMP_DIR}/log.txt
QEMU_RECORD_DUMP=${QEMU_DUMP_DIR}/record.bin
QEMU_PID_DUMP=${QEMU_DUMP_DIR}/pid.txt


QEMU_DIR=${ROOT_DIR}/qemu/master/x64/install/usr/local/
QEMU_ARM64=${QEMU_DIR}/bin/qemu-system-aarch64
QEMU_BRIDGE_HELPER=${QEMU_DIR}/libexec/qemu-bridge-helper

QEMU_EFI_DIR=${ROOT_DIR}/tianocore/edk2/master/Build/ArmVirtQemu-AARCH64/DEBUG_GCC5/FV/
QEMU_EFI_ARM64=${QEMU_EFI_DIR}/QEMU_EFI-pflash.raw
QEMU_VARS_ARM64=${QEMU_EFI_DIR}/QEMU_VARS-pflash.raw
QEMU_PARAMETERS_EFI_EXEC+=" -drive if=pflash,format=raw,readonly=on,file=${QEMU_EFI_ARM64},size=64M"
QEMU_PARAMETERS_EFI_VARS+=" -drive if=pflash,format=raw,file=${QEMU_VARS_ARM64},size=64M"
QEMU_PARAMETERS_EFI=${QEMU_PARAMETERS_EFI_EXEC}
QEMU_PARAMETERS_EFI+=${QEMU_PARAMETERS_EFI_VARS}

UBOOT_DIR=${ROOT_DIR}/u-boot/2024.10/aarch64/install/
UBOOT=${UBOOT_DIR}/u-boot.bin

INITRD=${ROOT_DIR}/images/artifacts/xen/dom0/rootfs.cpio.gz
ROOTFS=${ROOT_DIR}/images/artifacts/xen/dom0/rootfs.ext4

XEN_DIR=${ROOT_DIR}/yocto/dom0/product/tmp/deploy/images/qemuarm64/
XEN=${XEN_DIR}/xen-qemuarm64
XEN_EFI=${XEN_DIR}/xen-qemuarm64.efi
XEN_CMD_LINE="dom0_mem=3G,max:3G loglvl=all guest_loglvl=all console=dtuart"
# XEN_CMD_LINE+=" pci-passthrough=yes"

DOM0_MACHINE=qemuarm64
DOM0_TARGET=xen-image-minimal
DOM0_DIR=${ROOT_DIR}/yocto/dom0/product/tmp/deploy/images/${DOM0_MACHINE}/
DOM0_KERNEL=${DOM0_DIR}/Image
DOM0_KERNEL_CMD_LINE="root=/dev/ram verbose loglevel=7 console=hvc0 earlyprintk=xen"
# DOM0_KERNEL_CMD_LINE="root=/dev/vda verbose loglevel=7 console=hvc0 earlyprintk=xen"
DOM0_ROOTFS=${DOM0_DIR}/${DOM0_TARGET}-${DOM0_MACHINE}.rootfs.ext4
DOM0_INITRD=${DOM0_DIR}/${DOM0_TARGET}-${DOM0_MACHINE}.rootfs.cpio.gz

DOMD_MACHINE=qemuarm64
DOMD_TARGET=xen-guest-image-minimal
DOMD_DIR=${ROOT_DIR}/yocto/domd/product/tmp/deploy/images/${DOMD_MACHINE}/
DOMD_KERNEL=${DOMD_DIR}/Image
DOMD_KERNEL_CMD_LINE=""
DOMD_ROOTFS=${DOMD_DIR}/${DOMD_TARGET}-${DOMD_MACHINE}.rootfs.ext4
DOMD_INITRD=${DOMD_DIR}/${DOMD_TARGET}-${DOMD_MACHINE}.rootfs.cpio.gz



function qemu_run_help( )
{
   ${QEMU_ARM64} -help
   ${QEMU_ARM64} -d help
   # ${QEMU_ARM64} -machine virt -machine help
   # ${QEMU_ARM64} -machine virt -cpu help
   # ${QEMU_ARM64} -machine help
   # ${QEMU_ARM64} -device help
}

function build_params( )
{
   Q_MACHINE=" -machine virt"
   Q_MACHINE+=",acpi=off"
   Q_MACHINE+=",secure=off"
   Q_MACHINE+=",mte=on"
   # Q_MACHINE+=",accel=kvm"
   Q_MACHINE+=",virtualization=on"
   Q_MACHINE+=",iommu=smmuv3"
   Q_MACHINE+=",gic-version=max"
   # Q_MACHINE+=",its=off"
   # Q_MACHINE+=" -enable-kvm

   Q_CPU=" -cpu max,sme=off"
   Q_CPU+=" -smp 4"

   Q_MEMORY=" -m 8G"

   Q_COMMON=""
   Q_COMMON+=" -nodefaults"
   Q_COMMON+=" -no-reboot"

   Q_LOGGING=""
   Q_LOGGING+=" -D ${QEMU_LOG_DUMP}"
   Q_LOGGING+=" -d guest_errors"
   Q_LOGGING+=",cpu"
   Q_LOGGING+=",cpu_reset"
   Q_LOGGING+=",out_asm"
   Q_LOGGING+=",in_asm"
   Q_LOGGING+=",int"
   # Q_LOGGING+=" -pidfile ${QEMU_PID_DUMP}"

   Q_RECORD=" -icount shift=auto,rr=record,rrfile=${QEMU_RECORD_DUMP}"

   Q_MONITOR+=" -monitor tcp:127.0.0.1:4444,server,nowait"

   Q_KERNEL=" -kernel ${XEN}"
   Q_APPEND=" -append \"${XEN_CMD_LINE}\""
   Q_INITRD=" -initrd ${DOM0_INITRD}"
   Q_DTB=" -dtb ${DTB}"

   Q_GUEST_LOADER_DOM0_KERNEL=" \
      -device guest-loader,addr=0x60000000,kernel=${DOM0_KERNEL},bootargs=\"${DOM0_KERNEL_CMD_LINE}\" \
   "
   Q_GUEST_LOADER_DOM0_INITRD=" \
      -device guest-loader,addr=0x52000000,initrd=${DOM0_INITRD} \
   "

   Q_SERIAL=" -serial mon:stdio"

   Q_GRAPHIC=" -nographic"

   Q_PCI_BRIDGE=" -device pci-bridge,id=bridge0,chassis_nr=1"

   Q_DRIVE_DOM0_ROOTFS=" -drive if=none,index=0,id=rootfs_dom0,file=${DOM0_ROOTFS}"
   # Q_DRIVE_DOM0_ROOTFS+=" -device virtio-blk-pci,modern-pio-notify=off,drive=rootfs_dom0,bus=bridge0,addr=0x1"
   # Q_DRIVE_DOM0_ROOTFS+=" -device virtio-blk-pci,modern-pio-notify=off,drive=rootfs_dom0"
   Q_DRIVE_DOM0_ROOTFS+=" -device virtio-blk-device,drive=rootfs_dom0"

   Q_DRIVE_DOMD_ROOTFS=" -drive if=none,index=1,id=rootfs_domd,file=${DOMD_ROOTFS}"
   # Q_DRIVE_DOMD_ROOTFS+=" -device virtio-blk-pci,modern-pio-notify=off,drive=rootfs_domd,bus=bridge0,addr=0x2"
   # Q_DRIVE_DOMD_ROOTFS+=" -device virtio-blk-pci,modern-pio-notify=off,drive=rootfs_domd"
   Q_DRIVE_DOMD_ROOTFS+=" -device virtio-blk-device,drive=rootfs_domd"

   Q_NETWORK_NETDEV_USER=" \
      -netdev user,id=eth0_inet,hostfwd=tcp::5550-:5555,ipv6=off \
      -device virtio-net-pci,netdev=eth0_inet,id=android \
   "

   Q_NETWORK_NETDEV_BRIDGE=" \
      -netdev bridge,id=eth0_inet,br=virbr0,helper=${QEMU_BRIDGE_HELPER} \
      -device virtio-net-pci,netdev=eth0_inet,id=android \
   "

   Q_NETWORK_NETDEV_TAP=" \
      -netdev tap,id=eth0_inet,ifname=ethernet_tap,script=no,downscript=no,vhost=on \
      -device virtio-net-pci-non-transitional,netdev=eth0_inet,id=android \
   "

   Q_DEVICE_NET=${Q_NETWORK_NETDEV_USER}

   COMMAND="${QEMU_ARM64}"
   COMMAND+=" ${Q_MACHINE}"
   COMMAND+=" ${Q_CPU}"
   COMMAND+=" ${Q_MEMORY}"
   COMMAND+=" ${Q_COMMON}"
   # COMMAND+=" ${Q_LOGGING}"
   # COMMAND+=" ${Q_RECORD}"
   # COMMAND+=" ${Q_MONITOR}"
   COMMAND+=" ${Q_KERNEL}"
   COMMAND+=" ${Q_APPEND}"
   # COMMAND+=" ${Q_INITRD}"
   # COMMAND+=" ${Q_DTB}"
   COMMAND+=" ${Q_GUEST_LOADER_DOM0_KERNEL}"
   COMMAND+=" ${Q_GUEST_LOADER_DOM0_INITRD}"
   COMMAND+=" ${Q_SERIAL}"
   # COMMAND+=" -device pcie-root-port,id=root,slot=0"
   # COMMAND+=" ${Q_PCI_BRIDGE}"
   # COMMAND+=" ${Q_DRIVE_DOM0_ROOTFS}"
   COMMAND+=" ${Q_DRIVE_DOMD_ROOTFS}"
   # COMMAND+=" ${Q_DEVICE_NET}"
   # COMMAND+=" -s -S"

   echo "${COMMAND}"
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



LD_LIBRARY_PATH+=":${QEMU_DIR}/lib/"
LD_LIBRARY_PATH+=":${QEMU_DIR}/lib/x86_64-linux-gnu/"
COMMAND="export LD_LIBRARY_PATH"
print_ok "${COMMAND}"
eval "${COMMAND}"

qemu_run_help
# exit 0



COMMAND=$( build_params )

print_ok "${COMMAND} -machine dumpdtb=${QEMU_DTB_DUMP}"
eval "${COMMAND} -machine dumpdtb=${QEMU_DTB_DUMP}"

decompile_dt ${QEMU_DTB_DUMP} ${QEMU_DTS_DUMP}
compile_dt ${QEMU_DTS_DUMP} ${QEMU_DTB_DUMP_RECOMPILE}

print_ok "${COMMAND}"
echo ${COMMAND} > ${QEMU_COMMAND_DUMP}
eval "${COMMAND}"
