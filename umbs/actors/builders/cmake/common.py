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

      self.__graphviz_dir = os.path.join(
            self.__component_dir, self.__get_config( "graphviz" )
         ) if "graphviz" in self.__config else None
      self.__variables = self.__get_config( "variables", [ ] )
      self.__targets = self.__get_config( "targets", [ ] )
      self.__jobs = self.__get_config( "jobs", None )
   # def __init__

   def config( self, **kwargs ):
      command = "cmake"
      command += f" -S {self.__target_dir}"
      command += f" -B {self.__product_dir}"
      command += f" --install-prefix {self.__deploy_dir}"
      command += f" --graphviz={self.__graphviz_dir}" if self.__graphviz_dir else ""
      for variable in self.__variables:
         command += f" -D {variable}"

      return 0 == self.execute( command )["code"]
   # def config

   def build( self, **kwargs ):
      kw_targets = kwargs.get( "targets", self.__targets )

      command = "cmake"
      command += f" --build {self.__product_dir}"
      command += f" -j{self.__jobs}" if self.__jobs else ""
      if None != self.__targets:
         for target in self.__targets:
            command += f" --target {target}"

      return 0 == self.execute( command )["code"]
   # def build

   def deploy( self, **kwargs ):
      return True
      command = "cmake"
      command += f" --install {self.__product_dir}"
      # command += f" --target install"

      return 0 == self.execute( command )["code"]
   # def deploy

   def clean( self, **kwargs ):
      command = "cmake"
      command += f" --build {self.__product_dir}"
      command += f" --target clean"
      if 0 != self.execute( command )["code"]:
         return False

      command = f"rm -rf"
      command += f" {self.__product_dir}/CMakeFiles"
      command += f" {self.__product_dir}/CMakeCache.txt"
      command += f" {self.__product_dir}/Makefile"
      command += f" {self.__product_dir}/install_manifest.txt"
      command += f" {self.__product_dir}/cmake_install.cmake"
      if 0 != self.execute( command )["code"]:
         return False

      return True
   # def clean
# class Actor
