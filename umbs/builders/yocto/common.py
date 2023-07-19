import os

import pfw.console
import pfw.shell

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )
# def get_instance



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      strict_fields = [ "target" ]
      for key in strict_fields:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in builder" )

      self.__target = self.__config["target"]
   # def __init__

   def config( self, **kwargs ):
      command = f""
      return 0 == self.__execute( command )["code"]
   # def config

   def build( self, **kwargs ):
      command = f"bitbake"
      command += f" --verbose"
      command += f" {self.__target}"
      return 0 == self.__execute( command )["code"]
   # def build

   def clean( self, **kwargs ):
      return True
   # def clean

   def __execute( self, command ):
      cmd = f"source oe-init-build-env {self.__product_dir}"
      if command and 0 < len( command ):
         cmd += f" && {command}"
      return self.execute( cmd )
   # def __execute
# class Builder
