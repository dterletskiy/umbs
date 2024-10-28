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
      self.__defconfig = self.__get_config( "defconfig", None )
      self.__jobs = self.__get_config( "jobs", None )
      self.__arch = self.__get_config( "arch", None )
      self.__compiler = self.__get_config( "compiler", None )
   # def __init__

   def config( self, **kwargs ):
      result = self.execute( self.build_command( ), self.__defconfig, print = False, collect = False )
      if 0 != result["code"]:
         return False
      # self.execute( self.build_command( ), "menuconfig", print = False, collect = False )
      # self.execute( self.build_command( ), "savedefconfig", print = False, collect = False )

      return True
   # def config

   def build( self, **kwargs ):
      return 0 == self.execute( self.build_command( ), self.__targets )["code"]
   # def build

   def deploy( self, **kwargs ):
      result = self.execute( self.build_command( ), "install" )
      if 0 != result["code"]:
         return False

      result = self.execute( self.build_command( ), "modules_install" )
      if 0 != result["code"]:
         return False

      result = self.execute( self.build_command( ), "headers_install" )
      if 0 != result["code"]:
         return False

      return True
   # def deploy

   def clean( self, **kwargs ):
      result = self.execute( self.build_command( ), "clean distclean mrproper" )
      if 0 != result["code"]:
         return False

      return True
   # def clean

   def build_command( self, **kwargs ):
      command = f"export INSTALL_PATH={self.__deploy_dir};"
      command += f" export INSTALL_MOD_PATH={self.__deploy_dir};"
      command += f" make"
      command += f" O={self.__product_dir}"
      command += f" -C {self.__target_dir}"
      command += f" V=1"
      command += f" -j{self.__jobs}" if self.__jobs else ""
      command += f" ARCH={self.__arch}" if self.__arch else ""
      command += f" CROSS_COMPILE={self.__compiler}" if self.__compiler else ""

      return command
   # def build_command
# class Actor
