#!/usr/bin/env bash



readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# SHELL_FW=${SCRIPT_DIR}/submodules/dterletskiy/shell_fw/
SHELL_FW=${SCRIPT_DIR}/../sfw/
source ${SHELL_FW}/constants/console.sh
source ${SHELL_FW}/constants/constants.sh
source ${SHELL_FW}/base.sh
source ${SHELL_FW}/print.sh

readonly TEST=1



function run_umbs( )
{
   local CONFIGURATION=${1}

   COMMAND="./umbs.py ${CONFIGURATION}"

   print_text_in_bunner "${COMMAND}"

   if [[ 0 -eq ${TEST} ]]; then
      cd ${SCRIPT_DIR}
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

build_arc_in_container_x_all
