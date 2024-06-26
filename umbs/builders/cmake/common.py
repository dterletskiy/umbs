import os

import pfw.console
import pfw.shell

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( umbs.builders.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__graphviz_dir = os.path.join( self.__component_dir, self.__config["graphviz"] ) if "graphviz" in self.__config else None
      self.__variables = [ variable for variable in self.__config.get( "variables", [ ] ) ]
   # def __init__

   def config( self, **kwargs ):
      command = "cmake"
      command += f" -S {self.__target_dir}"
      command += f" -B {self.__product_dir}"
      command += f" --install-prefix {self.__deploy_dir}"
      command += f" --graphviz={self.__graphviz_dir}" if self.__graphviz_dir else ""
      for variable in self.__variables:
         command += f" -D {variable}"
      result = self.execute( command )
      if 0 != result["code"]:
         return False

      return True
   # def config

   def build( self, **kwargs ):
      kw_targets = kwargs.get( "targets", None )

      command = "cmake"
      command += f" --build {self.__product_dir}"
      command += f" -j{str( self.__config['jobs'] )}" if "jobs" in self.__config else ""
      if None != kw_targets:
         for target in kw_targets:
            command += f" --target {target}"
      result = self.execute( command )
      if 0 != result["code"]:
         return False

      return True
   # def build

   def deploy( self, **kwargs ):
      command = "cmake"
      command += f" --install {self.__product_dir}"
      # command += f" --target install"
      result = self.execute( command )
      if 0 != result["code"]:
         return False

      return True
   # def deploy

   def clean( self, **kwargs ):
      command = "cmake"
      command += f" --build {self.__product_dir}"
      command += f" --target clean"
      result = self.execute( command )
      if 0 != result["code"]:
         return False

      command = f"rm -rf"
      command += f" {self.__product_dir}/CMakeFiles"
      command += f" {self.__product_dir}/CMakeCache.txt"
      command += f" {self.__product_dir}/Makefile"
      command += f" {self.__product_dir}/install_manifest.txt"
      command += f" {self.__product_dir}/cmake_install.cmake"
      result = self.execute( command )
      if 0 != result["code"]:
         return False

      return True
   # def clean
# class Actor
