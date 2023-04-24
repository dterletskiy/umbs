import os

import pfw.console
import pfw.archive
import pfw.shell

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )

def do_build( builder ):
   builder.config( )
   builder.build( )
   builder.test( )

def do_clean( builder ):
   builder.clean( )



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__target = self.__config['config']
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def config( self, **kwargs ):
      command = f""

      pfw.shell.execute( command, cwd = self.__target_dir, print = False, collect = False )
   # def config

   def build( self, **kwargs ):
      command = f"tools/bazel run --sandbox_debug {self.__target}_dist -- --dist_dir=out/deploy/{self.__target}"

      pfw.shell.execute( command, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
   # def build

   def clean( self, **kwargs ):
      command = f"tools/bazel clean --expunge"

      pfw.shell.execute( command, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
   # def clean
# class Builder
