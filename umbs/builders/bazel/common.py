import os

import pfw.console
import pfw.archive
import pfw.shell

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )
# def get_instance



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__target = self.__config['config']

      self.__tool = self.__config.get( "tool", "bazel" )

      startup_options = self.__config.get( "startup_options", [ ] )
      startup_options.append( f"--output_root={self.__product_dir}" )
      self.__startup_options = " ".join( startup_options )

      self.__command = self.__config['command']

      self.__args = " ".join( self.__config.get( "args", [ ] ) )

      self.__target_patterns = " ".join( self.__config.get( "target_patterns", [ ] ) )
   # def __init__

   def config( self, **kwargs ):
      command = f""
      result = self.execute( command, print = False, collect = False )
      if 0 != result["code"]:
         return False

      return True
   # def config

   def build( self, **kwargs ):
      result = self.__execute(
            self.__command,
            starup_options = self.__startup_options,
            args = self.__args,
            target = self.__target,
            target_patterns = self.__target_patterns,
         )
      if 0 != result["code"]:
         return False

      return True
   # def build

   def clean( self, **kwargs ):
      result = self.__execute( "clean", args = "--expunge" )
      if 0 != result["code"]:
         return False

      return True
   # def clean

   def __execute( self, command, **kwargs ):
      kw_starup_options = kwargs.get( "starup_options", "" )
      kw_args = kwargs.get( "args", "" )
      kw_target = kwargs.get( "target", "" )
      kw_target_patterns = kwargs.get( "target_patterns", "" )

      cmd = f"{self.__tool}"
      cmd += f" {kw_starup_options}"
      cmd += f" {command}"
      cmd += f" {kw_args}"
      cmd += f" {kw_target}"
      cmd += f" -- {kw_target_patterns}" if 0 < len( kw_target_patterns ) else ""
      return self.execute( cmd )
   # def __execute
# class Builder
