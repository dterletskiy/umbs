#!/usr/bin/python

import os
import pfw.linux.qemu

def run_qemu( ):
   yocto_artifacts = "/mnt/dev/docker/builder/yocto/build/tmp/deploy/images/qemux86-64/"
   kernel = os.path.join( yocto_artifacts, "bzImage" )
   rootfs = os.path.join( yocto_artifacts, "core-image-minimal-qemux86-64.ext4" )
   append = "loop.max_loop=8 loglevel=7 printk.devkmsg=on console=ttyS0,38400 root=/dev/vda rw"

   PARAMETERS = f""
   PARAMETERS += f" -serial mon:stdio"
   PARAMETERS += f" -nodefaults"
   PARAMETERS += f" -no-reboot"
   PARAMETERS += f" -d guest_errors"

   IMAGE_DEVICES = f"" \
      + f" -drive if=none,index=0,id=main,file={rootfs}" \
      + f" -device virtio-blk-pci,modern-pio-notify=on,drive=main"

   parameters: str = f" {PARAMETERS}"
   parameters += f" {IMAGE_DEVICES}"

   pfw.linux.qemu.run(
         parameters,
         arch = "x86_64",
         kernel = kernel,
         append = append,
      )
# def run_qemu

run_qemu( )
