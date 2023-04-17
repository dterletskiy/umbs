import os
import re

import pfw.console
import pfw.shell

import umbs.base
import umbs.tools.base



def get_tool( config, directory, **kwargs ):
   return Tool( config, directory, **kwargs )

def do_exec( tool ):
   tool.exec( )
   tool.test( )

def do_clean( tool ):
   tool.clean( )



class Tool( umbs.tools.base.Tool ):
   def __init__( self, config, directory, **kwargs ):
      super( ).__init__( config, directory, **kwargs )

      for key in [ "exe", "source", "out" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      __exe = os.path.join( self.__root_dir, self.__config["exe"] )
      __source = os.path.join( self.__root_dir, self.__config["source"] )
      __out = os.path.join( self.__dir, self.__config["out"] )

      self.__command = f"mkdir -p {os.path.dirname( __out )};"
      self.__command += f" {__exe} {__source} {__out}"

      self.__out = __out
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def exec( self, **kwargs ):
      pfw.shell.execute( self.__command, output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def exec

   def clean( self, **kwargs ):
      pfw.shell.execute( f"rm {self.__out}", output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def clean
# class Tool
