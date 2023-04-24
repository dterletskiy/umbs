import os

import pfw.console
import pfw.shell

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

      for key in [ "content" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      self.__content = self.__config[ "content" ]
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
      for item in self.__content:
         pfw.shell.execute( f"rm {os.path.join( self.__target_dir, item['to'] )}", output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
   # def clean

   def exec( self, **kwargs ):
      for item in self.__content:
         pfw.linux.file.copy(
               os.path.join( self.__root_dir, item["from"] ),
               os.path.join( self.__target_dir, item["to"] ),
               force = True
            )
   # def exec
# class Tool
