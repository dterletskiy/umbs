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
      self.__params_config = ' '.join( self.__get_config( "params.config", [""] ) )
      self.__params_build = ' '.join( self.__get_config( "params.build", [""] ) )
   # def __init__

   def config( self, **kwargs ):
      command = "./configure"
      command += f" --cross-prefix={self.__compiler}" if self.__compiler else ""
      return 0 == self.execute( "./configure", self.__params_config, print = False, collect = False )["code"]
   # def config

   def build( self, **kwargs ):
      return 0 == self.execute( self.build_command( ), self.__params_build, self.__targets )["code"]
   # def build

   def deploy( self, **kwargs ):
      return 0 == self.execute( "make", "install", f"DESTDIR={self.__deploy_dir}" )["code"]
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

      return command
   # def build_command
# class Actor
