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

      self.__variables = [ variable for variable in self.__config.get( "variables", [ ] ) ]
   # def __init__

   def config( self, **kwargs ):
      command = "cmake"
      command += f" -S ${self.__target_dir}"
      command += f" -B ${self.__product_dir}"
      command += f" --install-prefix ${self.__deploy_dir}"
      command += " -D".join( self.__variables )
      result = pfw.shell.execute( command, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      if 0 != result["code"]:
         return False

      return True
   # def config

   def build( self, **kwargs ):
      command = "cmake"
      command += f" --build ${self.__product_dir}"
      command += f" -j{str( self.__config['jobs'] )}" if "jobs" in self.__config else ""
      result = pfw.shell.execute( command, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      if 0 != result["code"]:
         return False

      return True
   # def build

   def clean( self, **kwargs ):
      return True
   # def clean

   def build_command( self, **kwargs ):
      command = "make"
      return command
   # def build_command
# class Builder
