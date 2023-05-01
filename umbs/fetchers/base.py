import os

import pfw.console
import pfw.shell
import pfw.base.dict



class Fetcher:
   def __init__( self, config, **kwargs ):
      self.__config = config
      self.__root_dir = kwargs.get( "root_dir", None )
      self.__project_dir = kwargs.get( "project_dir", None )
      self.__target_dir = os.path.join( self.__project_dir, self.__config.get( "subdir", "" ) )
      pfw.shell.execute( f"mkdir -p {self.__target_dir}" )

      self.__artifacts = [ os.path.join( self.__project_dir, artifact ) for artifact in self.__config.get( "artifacts", [ ] ) ]
   # def __init__

   def __del__( self ):
      pass
   # def __del__

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

   def fetch( self, **kwargs ):
      pass
   # def fetch

   def remove( self, **kwargs ):
      pass
   # def remove

   def test( self, **kwargs ):
      result: bool = True

      for artifact in self.__artifacts:
         if os.path.exists( artifact ):
            pfw.console.debug.ok( f"artifact '{artifact}' exists" )
            pfw.shell.execute( f"file {artifact}", output = pfw.shell.eOutput.PTY )
         else:
            pfw.console.debug.error( f"artifact '{artifact}' does not exist" )
            result = False

      return result
   # def test



   def __get_config( self, keys ):
      return pfw.base.dict.get_value( self.__config, keys )
   # def __get_config
# class Tool
