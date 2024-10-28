#!/usr/bin/env bash



readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

readonly DELIMITER_CHAR="-"
readonly SIDE_CHAR="|"
readonly SPACE_CHAR=" "

readonly BANNER_LENGTH=200

readonly DELIMITER_1="+"$(printf "%$(( BANNER_LENGTH - 2 ))s" | tr ' ' "${DELIMITER_CHAR}")"+"
readonly DELIMITER_1_LENGTH=$(echo -n "${DELIMITER_1}" | wc -c)

readonly DELIMITER_2="||"$(printf "%$(( BANNER_LENGTH - 4 ))s" | tr ' ' "${SPACE_CHAR}")"||"
readonly DELIMITER_2_LENGTH=$(echo -n "${DELIMITER_2}" | wc -c)

readonly TEST=1



function run_umbs( )
{
   local CONFIGURATION=${1}

   cd ${SCRIPT_DIR}
   COMMAND="./umbs.py ${CONFIGURATION}"
   COMMAND_LENGTH=$(echo -n "${COMMAND}" | wc -c)

   SIDE_SPACE_COUNT=$(( ( BANNER_LENGTH - COMMAND_LENGTH - 2 ) / 2 ))
   SIDE_SPACE=$(printf "%${SIDE_SPACE_COUNT}s" | tr ' ' "${SPACE_CHAR}")
   SPACE_ADD_COUNT=$(( ( BANNER_LENGTH - COMMAND_LENGTH - 2 ) % 2 ))
   SPACE_ADD=$(printf "%${SPACE_ADD_COUNT}s" | tr ' ' "${SPACE_CHAR}")

   printf "${DELIMITER_1}\n"
   printf "${DELIMITER_2}\n"
   printf "${DELIMITER_2}\n"
   printf "${SIDE_CHAR}${SIDE_SPACE}${COMMAND}${SIDE_SPACE}${SPACE_ADD}${SIDE_CHAR}\n"
   printf "${DELIMITER_2}\n"
   printf "${DELIMITER_2}\n"
   printf "${DELIMITER_1}\n"

   if [[ 0 -eq ${TEST} ]]; then
      eval "${COMMAND}"
   fi
}



function builder_arc_params( )
{
   local LOCAL_ARCH=${1}
   local LOCAL_KEY=${2}

   declare -A BUILDER_X64=(
         [name]="x64"
         [container]="builder_x64_ubuntu_22.04"
      )

   declare -A BUILDER_AARCH64=(
         [name]="aarch64"
         [container]="builder_arm64v8_ubuntu_22.04"
      )

   case ${LOCAL_ARCH} in
      x64)
         declare -n BUILDER=BUILDER_X64
      ;;
      aarch64)
         declare -n BUILDER=BUILDER_AARCH64
      ;;
      *)
         echo "Undefined architecture: '${LOCAL_ARCH}'"
         exit 1
      ;;
   esac

   echo ${BUILDER[${LOCAL_KEY}]}
}

function build_arc_in_container_x( )
{
   local LOCAL_COMPONENT=${1}
   local LOCAL_ACTION=${2}
   local LOCAL_ARCH=${3}

   local LOCAL_ARCH_NAME=$(builder_arc_params ${LOCAL_ARCH} name)
   local LOCAL_CONTAINER=$(builder_arc_params ${LOCAL_ARCH} container)

   local LOCAL_CONFIGURATION=""
   LOCAL_CONFIGURATION+=" --config=./configuration/host.cfg"
   LOCAL_CONFIGURATION+=" --component=${LOCAL_COMPONENT}_${LOCAL_ARCH_NAME}"
   LOCAL_CONFIGURATION+=" --action=${LOCAL_ACTION}"
   LOCAL_CONFIGURATION+=" --container=${LOCAL_CONTAINER}"

   run_umbs "${LOCAL_CONFIGURATION}"
}

function build_arc_in_container_x_all( )
{
   build_arc_in_container_x xen world x64
   build_arc_in_container_x xen world aarch64

   build_arc_in_container_x uboot world x64
   build_arc_in_container_x uboot world aarch64

   build_arc_in_container_x qemu world x64
   build_arc_in_container_x qemu world aarch64

   build_arc_in_container_x kernel world x64
   build_arc_in_container_x kernel world aarch64
}



clear

# build_arc_in_container_x_all


# exit 0



QEMU_PATH=/mnt/dev/docker/builder/qemu/9.1/x64/install/usr/local/
QEMU_ARM64=${QEMU_PATH}/bin/qemu-system-aarch64
UBOOT=/mnt/dev/docker/builder/u-boot/2024.10/aarch64/install/u-boot.bin
DTB=/mnt/dev/docker/builder/#_workspace_#/qemu.dtb
# XEN=/mnt/dev/docker/builder/xen/4.19/aarch64/install/boot/xen
XEN=/mnt/dev/docker/builder/yocto/product/tmp/deploy/images/qemuarm64/xen-qemuarm64
XEN_CMD_LINE="dom0_mem=3G,max:3G loglvl=all guest_loglvl=all console=dtuart"
KERNEL=/mnt/dev/docker/builder/yocto/product/tmp/deploy/images/qemuarm64/Image
KERNEL_CMD_LINE="root=/dev/vda verbose loglevel=7 console=hvc0 earlyprintk=xen"
# INITRD=/mnt/dev/docker/builder/yocto/product/tmp/deploy/images/rootfs.cpio
INITRD=/mnt/dev/docker/builder/yocto/product/tmp/deploy/images/qemuarm64/xen-image-minimal-qemuarm64.rootfs.cpio.gz
ROOTFS=/mnt/dev/docker/builder/yocto/product/tmp/deploy/images/qemuarm64/xen-image-minimal-qemuarm64.rootfs.ext4

DRIVE_MAIN=/mnt/dev/docker/builder/images/drive/install/main.img


QEMU_EFI_PATH=/mnt/dev/docker/builder/tianocore/edk2/master/Build/ArmVirtQemu-AARCH64/DEBUG_GCC5/FV/
QEMU_EFI_ARM64=${QEMU_EFI_PATH}/QEMU_EFI-pflash.raw
QEMU_VARS_ARM64=${QEMU_EFI_PATH}/QEMU_VARS-pflash.raw
QEMU_PARAMETERS_EFI_EXEC+=" -drive if=pflash,format=raw,readonly=on,file=${QEMU_EFI_ARM64},size=64M"
QEMU_PARAMETERS_EFI_VARS+=" -drive if=pflash,format=raw,file=${QEMU_VARS_ARM64},size=64M"
QEMU_PARAMETERS_EFI=${QEMU_PARAMETERS_EFI_EXEC}
QEMU_PARAMETERS_EFI+=${QEMU_PARAMETERS_EFI_VARS}

LD_LIBRARY_PATH_QEMU="${QEMU_PATH}/lib/"
LD_LIBRARY_PATH_QEMU+=":${QEMU_PATH}/lib/x86_64-linux-gnu/"
echo export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LD_LIBRARY_PATH_QEMU}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LD_LIBRARY_PATH_QEMU}

# ${QEMU_ARM64} -machine virt -machine help
# ${QEMU_ARM64} -machine help
# ${QEMU_ARM64} -device help

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
   ROOTFS_DOMD=/mnt/dev/docker/builder/yocto/product/tmp/deploy/images/rootfs_domd.ext4

   QEMU_PARAMETERS=""
   QEMU_PARAMETERS+=" -machine virt,acpi=off,secure=off,mte=on,virtualization=on,iommu=smmuv3"
   # QEMU_PARAMETERS+=" -machine dumpdtb=/mnt/dev/docker/builder/#_workspace_#/qemu.dtb"
   QEMU_PARAMETERS+=" -cpu max,sme=off"
   # QEMU_PARAMETERS+=" -smp 4"
   QEMU_PARAMETERS+=" -m 8G"
   # QEMU_PARAMETERS+=" -d guest_errors"
   # QEMU_PARAMETERS+=" -nodefaults"
   QEMU_PARAMETERS+=" -nographic"
   QEMU_PARAMETERS+=" -no-reboot"
   QEMU_PARAMETERS+=" -kernel ${XEN}"
   QEMU_PARAMETERS+=" -append \"${XEN_CMD_LINE}\""
   QEMU_PARAMETERS+=" \
      -device guest-loader,addr=0x42000000,kernel=${KERNEL},bootargs=\"${KERNEL_CMD_LINE}\" \
   "
   # QEMU_PARAMETERS+=" \
   #    -device guest-loader,addr=0x47000000,initrd=${INITRD} \
   # "
   # QEMU_PARAMETERS+=" -initrd ${INITRD}"

   QEMU_PARAMETERS+=" -drive if=none,index=0,id=rootfs,file=${ROOTFS}"
   # QEMU_PARAMETERS+=" -device virtio-blk-pci,modern-pio-notify=on,drive=rootfs"
   QEMU_PARAMETERS+=" -device virtio-blk-device,drive=rootfs"

   QEMU_PARAMETERS+=" -drive if=none,index=1,id=main,file=${DRIVE_MAIN}"
   QEMU_PARAMETERS+=" -device virtio-blk-pci,modern-pio-notify=on,drive=main"

   QEMU_PARAMETERS+=" -drive if=none,index=2,id=rootfs_domd,file=${ROOTFS_DOMD}"
   QEMU_PARAMETERS+=" -device virtio-blk-pci,modern-pio-notify=on,drive=rootfs_domd"

   # QEMU_PARAMETERS+=" -device smmuv3"
   # QEMU_PARAMETERS+=" -device arm-smmu"

   COMMAND="${QEMU_ARM64} ${QEMU_PARAMETERS}"
   echo ----------------------------------------------------------------------------------------------------
   echo "${COMMAND}"
   echo ----------------------------------------------------------------------------------------------------
   eval "${COMMAND}"
}

function print_setenv_var_size( )
{
   local VAR_NAME=${1}
   declare -n VAR_VALUE=${1}

   SIZE=$(stat -c%s "${VAR_VALUE}")
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
   ROOTFS=/mnt/dev/docker/builder/yocto/product/tmp/deploy/images/rootfs_domd.ext4
   UBOOT=/mnt/dev/docker/builder/#_workspace_#/u-boot/2024.10/aarch64/u-boot.bin
   KERNEL=/mnt/dev/docker/builder/yocto/product/tmp/deploy/images/Image
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

qemu_run_02
