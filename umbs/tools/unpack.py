import os

import pfw.console
import pfw.shell
import pfw.archive

import umbs.base
import umbs.tools.base



def get_instance( config, **kwargs ):
   return Tool( config, **kwargs )
# def get_instance



class Tool( umbs.tools.base.Tool ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "file" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      self.__file = os.path.join( self.__project_dir, self.__config[ "file" ] )
   # def __init__

   def exec( self, **kwargs ):
      result = pfw.archive.extract( self.__file, None, self.__target_dir )
      return 0 == result["code"]
   # def exec

   def clean( self, **kwargs ):
      return True
   # def clean
# class Tool
