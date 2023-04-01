import os

import pfw.console
import pfw.archive
import pfw.shell



def get_builder( config, directory, **kwargs ):
   return Builder( config, directory, **kwargs )

def do_build( builder ):
   builder.config( )
   builder.build( )
   builder.test( )

def do_clean( builder ):
   builder.clean( )



class Builder:
   def __init__( self, config, directory, **kwargs ):
      self.__root_dir = kwargs.get( "root_dir", None )

      self.__config = config
      self.__dir = directory

      self.__artifacts = [ os.path.join( self.__dir, artifact ) for artifact in self.__config.get( "artifacts", [ ] ) ]
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __setattr__( self, attr, value ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) ]
      if attr in attr_list:
         self.__dict__[ attr ] = value
         return
      raise AttributeError
   # def __setattr__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def info( self, **kwargs ):
      kw_tabs = kwargs.get( "tabs", 0 )
      kw_msg = kwargs.get( "msg", "" )
      pfw.console.debug.info( f"{kw_msg} (type {self.__class__.__name__}):", tabs = ( kw_tabs + 0 ) )
   # def info

   def config( self, **kwargs ):
      command = f""

      pfw.shell.execute( command, cwd = self.__dir, print = False, collect = False )
   # def config

   def build( self, **kwargs ):
      command = f"tools/bazel run --sandbox_debug {self.__config['config']}_dist -- --dist_dir=out/deploy/{self.__config['config']}"

      pfw.shell.execute( command, output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def build

   def clean( self, **kwargs ):
      command = f""

      pfw.shell.execute( command, output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def clean

   def deploy( self, **kwargs ):
      pass
   # def deploy

   def test( self, **kwargs ):
      result: bool = True

      for artifact in self.__artifacts:
         if os.path.exists( artifact ):
            pfw.console.debug.ok( f"artifact '{artifact}' exists" )
         else:
            pfw.console.debug.error( f"artifact '{artifact}' does not exist" )
            result = False

      return result
   # def test



   __config: dict = None
   __dir: str = None
   __root_dir: str = None
   __artifacts: list = [ ]
# class Builder
