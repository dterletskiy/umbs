import os

import pfw.console
import pfw.shell

import umbs.base
import umbs.tools.base



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( umbs.tools.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "kernel", "ramdisk", "out" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )

      __exe = "mkbootimg"
      if "exe" in self.__config:
         __exe = os.path.join( self.__root_dir, self.__config["exe"] )
      __kernel = os.path.join( self.__root_dir, self.__config["kernel"] )
      __ramdisk = os.path.join( self.__root_dir, self.__config["ramdisk"] )
      __dtb = self.__config.get( "dtb", None )
      __second = self.__config.get( "second", None )
      __header_version = self.__config.get( "header_version", None )
      __os_version = self.__config.get( "os_version", None )
      __os_patch_level = self.__config.get( "os_patch_level", None )
      __cmdline = self.__config.get( "cmdline", None )
      __base = self.__config.get( "base", None )
      __kernel_offset = self.__config.get( "kernel_offset", None )
      __ramdisk_offset = self.__config.get( "ramdisk_offset", None )
      __dtb_offset = self.__config.get( "dtb_offset", None )
      __vendor_ramdisk = self.__config.get( "vendor_ramdisk", None )
      __vendor_cmdline = self.__config.get( "vendor_cmdline", None )
      __vendor_bootconfig = self.__config.get( "vendor_bootconfig", None )
      __vendor_boot = self.__config.get( "vendor_boot", None )

      __out = os.path.join( self.__target_dir, self.__config["out"] )

      command: str = f" {exe}"
      command += f" --header_version {__header_version}"
      command += f" --os_version {__os_version}"
      command += f" --os_patch_level {__os_patch_level}"
      command += f" --kernel {__kernel}"
      command += f" --ramdisk {__ramdisk}"
      command += f" --dtb {__dtb}" if __dtb else ""
      command += f" --second {__second}" if __second else ""
      command += f" --cmdline \"{__cmdline}\"" if __cmdline else ""
      command += f" --base {__base}" if __base else ""
      command += f" --kernel_offset {__kernel_offset}" if __kernel_offset else ""
      command += f" --ramdisk_offset {__ramdisk_offset}" if __ramdisk_offset else ""
      command += f" --dtb_offset {__dtb_offset}" if __dtb_offset else ""
      command += f" --vendor_ramdisk {__vendor_ramdisk}" if __vendor_ramdisk else ""
      command += f" --vendor_cmdline {__vendor_cmdline}" if __vendor_cmdline else ""
      command += f" --vendor_bootconfig {__vendor_bootconfig}" if __vendor_bootconfig else ""
      command += f" --vendor_boot {__vendor_boot}" if __vendor_boot else ""
      command += f" --out {__out}"

      self.__out = __out
   # def __init__

   def exec( self, **kwargs ):
      result = pfw.shell.execute( self.__command, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      return 0 == result["code"]
   # def exec

   def clean( self, **kwargs ):
      result = pfw.shell.execute( f"rm {self.__out}", output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      return 0 == result["code"]
   # def clean
# class Actor
