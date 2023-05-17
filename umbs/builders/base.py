import os

import pfw.console
import pfw.shell
import pfw.base.dict



class Builder:
   def __init__( self, config, **kwargs ):
      self.__config = config
      self.__root_dir = kwargs.get( "root_dir", None )
      self.__project_dir = kwargs.get( "project_dir", None )
      self.__target_dir = os.path.join( self.__project_dir, self.__config.get( "subdir", "" ) )
      self.__product_dir = os.path.join( self.__project_dir, self.__config.get( "product_subdir", "" ) )
      self.__deploy_dir = os.path.join( self.__project_dir, self.__config.get( "deploy_subdir", "" ) )

      self.__artifacts = [ os.path.join( self.__project_dir, artifact ) for artifact in self.__config.get( "artifacts", [ ] ) ]

      self.__dependencies = [ os.path.join( self.__project_dir, dependency ) for dependency in self.__config.get( "deps", [ ] ) ]

      # self.__dependencies = [ ]
      # for dependency in self.__config.get( "deps", [ ] ):
      #    if isinstance( dependency, str ):
      #       self.__dependencies.append( os.path.join( self.__root_dir, dependency ) )
      #    elif isinstance( dependency, dict ):
      #       # self.__dependencies.append( os.path.join( dependency[key].project_dir( ), dependency[value] ) )
      #       pass
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

   def prepare( self, **kwargs ):
      result = pfw.shell.execute( f"mkdir -p {self.__target_dir}" )
      if 0 != result["code"]:
         return False

      result = pfw.shell.execute( f"mkdir -p {self.__product_dir}" )
      if 0 != result["code"]:
         return False

      result = pfw.shell.execute( f"mkdir -p {self.__deploy_dir}" )
      if 0 != result["code"]:
         return False

      return True
   # def prepare

   def config( self, **kwargs ):
      return True
   # def config

   def build( self, **kwargs ):
      return True
   # def build

   def clean( self, **kwargs ):
      return True
   # def clean

   def deploy( self, **kwargs ):
      return True
   # def deploy

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



   def project_dir( self ):
      return self.__project_dir
   # def project_dir

   def target_dir( self ):
      return self.__target_dir
   # def target_dir

   def product_dir( self ):
      return self.__product_dir
   # def product_dir

   def deploy_dir( self ):
      return self.__deploy_dir
   # def deploy_dir

   def artifacts( self ):
      return self.__artifacts
   # def artifacts

   def dependencies( self ):
      return self.__dependencies
   # def dependencies
# class Builder
