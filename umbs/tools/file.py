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

      for key in [ "location", "name", "content" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      self.__file = os.path.join(
            self.__component_dir, self.__config[ "location" ], self.__config[ "name" ]
         )
      self.__content = self.__config[ "content" ]
      self.__mode = "w"
   # def __init__

   def exec( self, **kwargs ):
      result = False
      with open( self.__file, self.__mode ) as fd:
         fd.write( "\n".join( self.__content ) )
         result = True

      return result
   # def exec

   def clean( self, **kwargs ):
      result = True

      return result
   # def clean
# class Actor
