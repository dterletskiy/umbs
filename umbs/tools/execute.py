import os

import pfw.console
import pfw.shell
import pfw.linux.file

import umbs.base
import umbs.tools.base



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( umbs.tools.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "command" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      self.__command = self.__config[ "command" ]
      self.__parameters = self.__config.get( "parameters", [ ] )
   # def __init__

   def exec( self, **kwargs ):
      return 0 == pfw.shell.execute2( self.__command, *self.__parameters )["code"]
   # def exec
# class Actor
