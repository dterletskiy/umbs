import os

import pfw.console
import pfw.shell
import pfw.linux.archive

import umbs.base
import umbs.tools.base



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( umbs.tools.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "file" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      self.__file = os.path.join( self.__component_dir, self.__config[ "file" ] )
      self.__format = self.__config.get( "format", None )
   # def __init__

   def exec( self, **kwargs ):
      result = pfw.linux.archive.unpack( self.__file, self.__target_dir, self.__format )
      return 0 == result
   # def exec

   def clean( self, **kwargs ):
      return True
   # def clean
# class Actor
