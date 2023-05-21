import os
import re

import pfw.console
import pfw.shell

import umbs.base
import umbs.tools.base



def get_instance( config, **kwargs ):
   return Tool( config, **kwargs )
# def get_instance



class Tool( umbs.tools.base.Tool ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "exe", "source", "out" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      __exe = os.path.join( self.__root_dir, self.__config["exe"] )
      __source = os.path.join( self.__root_dir, self.__config["source"] )
      __out = os.path.join( self.__target_dir, self.__config["out"] )

      self.__command = f"mkdir -p {os.path.dirname( __out )};"
      self.__command += f" {__exe} {__source} {__out}"

      self.__out = __out
   # def __init__

   def exec( self, **kwargs ):
      result = pfw.shell.execute( self.__command, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      return 0 == result["code"]
   # def exec

   def clean( self, **kwargs ):
      result = pfw.shell.execute( f"rm {self.__out}", output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      return 0 == result["code"]
   # def clean
# class Tool
