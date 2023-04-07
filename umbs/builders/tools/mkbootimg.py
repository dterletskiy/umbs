import os

import pfw.console
import pfw.shell

import umbs.base



def get_builder( config, directory, **kwargs ):
   return Tool( config, directory, **kwargs )

def do_build( tool ):
   tool.build( )
   tool.test( )

def do_clean( tool ):
   tool.clean( )



class Tool:
   def __init__( self, config, directory, **kwargs ):
      self.__root_dir = kwargs.get( "root_dir", None )

      self.__config = config
      self.__dir = directory

      self.__artifacts = [ os.path.join( self.__dir, artifact ) for artifact in self.__config.get( "artifacts", [ ] ) ]

      for key in [ "exe", "kernel", "ramdisk", "out" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )

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

      __out = os.path.join( self.__dir, self.__config["out"] )

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

   def __del__( self ):
      pass
   # def __del__

   def __setattr__( self, attr, value ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) ]
      if attr in attr_list:
         self.__dict__[ attr ] = value
         return
      raise AttributeError
   # def __setattr__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def info( self, **kwargs ):
      kw_tabs = kwargs.get( "tabs", 0 )
      kw_msg = kwargs.get( "msg", "" )
      pfw.console.debug.info( f"{kw_msg} (type {self.__class__.__name__}):", tabs = ( kw_tabs + 0 ) )
   # def info

   def clean( self, **kwargs ):
      pfw.shell.execute( f"rm {self.__out}", output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def clean

   def build( self, **kwargs ):
      pfw.shell.execute( self.__command, output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def build

   def test( self, **kwargs ):
      result: bool = True

      for artifact in self.__artifacts:
         if os.path.exists( artifact ):
            pfw.console.debug.ok( f"artifact '{artifact}' exists" )
            pfw.shell.execute( f"file {artifact}", output = pfw.shell.eOutput.PTY )
         else:
            pfw.console.debug.error( f"artifact '{artifact}' does not exist" )
            result = False

      return result
   # def test



   __config: dict = None
   __dir: str = None
   __root_dir: str = None
   __artifacts: list = [ ]

   __command: str = None
   __out: str = None
# class Tool
