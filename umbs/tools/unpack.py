import os

import pfw.console
import pfw.shell
import pfw.archive

import umbs.base
import umbs.tools.base



def get_instance( config, **kwargs ):
   return Tool( config, **kwargs )

def do_exec( tool ):
   tool.exec( )
   tool.test( )

def do_clean( tool ):
   tool.clean( )



class Tool( umbs.tools.base.Tool ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "file" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      self.__file = os.path.join( self.__project_dir, self.__config[ "file" ] )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def clean( self, **kwargs ):
      pass
   # def clean

   def exec( self, **kwargs ):
      pfw.archive.extract( self.__file, None, self.__target_dir )
   # def exec
# class Tool
