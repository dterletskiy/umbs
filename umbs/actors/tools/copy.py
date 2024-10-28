import importlib
import os

import pfw.console
import pfw.shell
import pfw.linux.file

import umbs.actors.types
module_tool_base = importlib.import_module( f"{umbs.actors.types.eType.TOOL}.base", __package__ )



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( module_tool_base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "content" ]:
         if key not in self.__config:
            raise pfw.base.yaml.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      self.__content = self.__get_config( "content" )
      for item in self.__content:
         if os.path.isabs( item["to"] ):
            raise pfw.base.yaml.YamlFormatError(
               f"Destination path '{item['to']}' must be relative to component directory '{self.__component_dir}'"
            )

         item["from"] = os.path.join( self.__component_dir, item["from"] )
         item["to"] = os.path.join( self.__component_dir, item["to"] )
   # def __init__

   def exec( self, **kwargs ):
      result = True
      for item in self.__content:
         result = result and pfw.linux.file.copy( item["from"], item["to"], force = True )

      return result
   # def exec

   def clean( self, **kwargs ):
      result = True
      for item in self.__content:
         result = result and pfw.linux.file.remove( item["to"], force = True )

      return result
   # def clean
# class Actor
