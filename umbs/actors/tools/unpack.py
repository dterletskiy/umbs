import importlib
import os

import pfw.console
import pfw.shell
import pfw.linux.archive

import umbs.actors.types
module_tool_base = importlib.import_module( f"{umbs.actors.types.eType.TOOL}.base", __package__ )



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( module_tool_base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "file", "format", "destination" ]:
         if key not in self.__config:
            raise pfw.base.yaml.YamlFormatError( f"Filed '{key}' must be defined in tool" )

      if os.path.isabs( self.__get_config( "destination" ) ):
         raise pfw.base.yaml.YamlFormatError(
            f"Destination path '{self.__get_config( 'destination' )}' must be relative to component directory '{self.__component_dir}'"
         )


      self.__file = os.path.join( self.__component_dir, self.__get_config( "file" ) )
      self.__format = self.__get_config( "format", None )
      self.__destination = os.path.join( self.__component_dir, self.__get_config( "destination" ) )
   # def __init__

   def exec( self, **kwargs ):
      return 0 == pfw.linux.archive.unpack( self.__file, self.__destination, self.__format )
   # def exec

   def clean( self, **kwargs ):
      return True
   # def clean
# class Actor
