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

      self.__config_cmd_line = "";
      # self.__config_cmd_line += f" export TARGET_PREBUILT_KERNEL=;"
      # self.__config_cmd_line += f" export TARGET_PREBUILT_MODULES_DIR=;"
      # self.__config_cmd_line += f" export OUT_DIR_COMMON_BASE=;"
      self.__config_cmd_line += f" source build/envsetup.sh;"
      self.__config_cmd_line += f" lunch {self.__config['config']};"

      self.__target = self.__config['config']
   # def __init__

   def config( self, **kwargs ):
      return True
   # def config

   def build( self, **kwargs ):
      command = f"make showcommands"
      return self.__execute( command, output = pfw.shell.eOutput.PIPE )
   # def build

   def clean( self, **kwargs ):
      command = f"make clean"
      return self.__execute( command, output = pfw.shell.eOutput.PIPE )
   # def clean



   def __execute( self, command: str = "", **kwargs ):
      kw_output = kwargs.get( "output", pfw.shell.eOutput.PTY )

      result = pfw.shell.execute( f"{self.__config_cmd_line} {command}", cwd = self.__target_dir, output = kw_output )
      return 0 == result["code"]
   # def __execute
# class Builder
