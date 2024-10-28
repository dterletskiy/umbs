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

      self.__targets = self.__get_config( "targets", [""] )
      self.__jobs = self.__get_config( "jobs", None )
      self.__arch = self.__get_config( "arch", None )
      self.__compiler = self.__get_config( "compiler", None )

      self.__targets_build = " ".join( f"dist-{word}" for target in self.__targets for word in target.split( ) )
      self.__targets_install = " ".join( f"install-{word}" for target in self.__targets for word in target.split( ) )
      self.__targets = " ".join( self.__targets )
   # def __init__

   def config( self, **kwargs ):
      return 0 == self.execute( "./configure", print = False, collect = False, cwd = self.__target_dir )["code"]
   # def config

   def build( self, **kwargs ):
      return 0 == self.execute( self.build_command( ), self.__targets, cwd = self.__target_dir )["code"]
   # def build

   def deploy( self, **kwargs ):
      return 0 == self.execute( "make", "install", f"DESTDIR={self.__deploy_dir}", cwd = self.__target_dir )["code"]
   # def deploy

   def clean( self, **kwargs ):
      return 0 == self.execute( self.build_command( ), "clean distclean mrproper", cwd = self.__target_dir )
   # def clean

   def build_command( self, **kwargs ):
      command = "make"
      command += f" -j{self.__jobs}" if self.__jobs else ""
      command += f" XEN_TARGET_ARCH={self.__arch}" if self.__arch else ""
      command += f" CROSS_COMPILE={self.__compiler}" if self.__compiler else ""

      return command
   # def build_command
# class Actor
