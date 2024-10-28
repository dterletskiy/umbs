import importlib
import os

import pfw.console
import pfw.shell

import umbs.actors.types
module_builder_base = importlib.import_module( f"{umbs.actors.types.eType.BUILDER}.base", __package__ )



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( module_builder_base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__targets = ' '.join( self.__get_config( "targets", ["all"] ) )
      self.__defconfig = self.__get_config( "defconfig", "defconfig" )
      self.__jobs = self.__get_config( "jobs", None )
      self.__compiler = self.__get_config( "compiler", None )
   # def __init__

   def config( self, **kwargs ):
      return 0 == self.execute( self.build_command( ), self.__defconfig, print = False, collect = False )["code"]
   # def config

   def build( self, **kwargs ):
      return 0 == self.execute( self.build_command( ), self.__targets )["code"]
   # def build

   def deploy( self, **kwargs ):
      artifacts = [
            "u-boot*",
            "rom.map",
            "System.map",
            "spl/u-boot*",
            "scripts/basic/fixdep",
            "scripts/dtc/dtc",
            "scripts/kconfig/conf",
            "tools/bmp_logo",
            "tools/dumpimage",
            "tools/fdt_add_pubkey",
            "tools/fdtgrep",
            "tools/file2include",
            "tools/fit_check_sign",
            "tools/fit_info",
            "tools/gen_eth_addr",
            "tools/gen_ethaddr_crc",
            "tools/ifdtool",
            "tools/ifwitool",
            "tools/img2srec",
            "tools/mkeficapsule",
            "tools/mkenvimage",
            "tools/mkimage",
            "tools/proftool",
            "tools/spl_size_limit",
         ]

      deploy_result: bool = True
      for artifact in artifacts:
         result = pfw.shell.execute(
               f"cp --parents {artifact} {self.__deploy_dir}",
               cwd = self.__product_dir
            )
         if 0 != result["code"]:
            deploy_result = False

      return True
   # def deploy

   def clean( self, **kwargs ):
      return 0 == self.execute( self.build_command( ), "clean distclean mrproper" )
   # def clean

   def build_command( self, **kwargs ):
      command = "make"
      command += f" O={self.__product_dir}"
      command += f" -C {self.__target_dir}"
      command += f" V=1"
      command += f" -j{self.__jobs}" if self.__jobs else ""
      command += f" CROSS_COMPILE={self.__compiler}" if self.__compiler else ""

      return command
   # def build_command
# class Actor
