import os

import pfw.console
import pfw.shell
import pfw.base.dict
import pfw.os.environment



class Builder:
   def __init__( self, config, **kwargs ):
      self.__config = config
      self.__root_dir = kwargs.get( "root_dir", None )
      self.__component_dir = kwargs.get( "component_dir", None )
      # target_dir <=> source code dir
      self.__target_dir = os.path.join(
            self.__component_dir,
            pfw.base.dict.get_value( self.__config, ["subdirs", "target"], "" )
         )
      # product_subdir <=> build code dir
      self.__product_dir = os.path.join(
            self.__component_dir,
            pfw.base.dict.get_value( self.__config, ["subdirs", "product"], "" )
         )
      # deploy_subdir <=> deploy code dir
      self.__deploy_dir = os.path.join(
            self.__component_dir,
            pfw.base.dict.get_value( self.__config, ["subdirs", "deploy"], "" )
         )

      self.__artifacts = [
            os.path.join( self.__component_dir, artifact ) for artifact in self.__config.get( "artifacts", [ ] )
         ]

      self.__dependencies = self.__config.get( "deps", [ ] )

      environment: dict = { }
      for env in self.__config.get( "env", [ ] ):
         env_list = env.split( "=" )
         if len( env_list ) not in [1, 2]:
            continue
         environment[ env_list[0] ] = env_list[1] if 2 == len( env_list ) else ""
      self.__environment = pfw.os.environment.build( env_add = environment )

      self.__export = ""
      for env in self.__config.get( "env", [ ] ):
         if 0 == len( env ):
            continue

         self.__export += f" export {env};"
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

   def do_build( self, **kwargs ):
      if not self.prepare( ):
         pfw.console.debug.error( "prepare error" )
         return False
      if not self.config( ):
         pfw.console.debug.error( "config error" )
         return False
      if not self.build( ):
         pfw.console.debug.error( "build error" )
         return False
      if not self.deploy( ):
         pfw.console.debug.error( "deploy error" )
         return False
      if not self.test( ):
         pfw.console.debug.error( "test error" )
         return False

      return True
   # def do_build

   def do_clean( self, **kwargs ):
      if not self.clean( ):
         pfw.console.debug.error( "clean error" )
         return False

      return True
   # def do_clean

   def prepare( self, **kwargs ):
      result = self.execute( f"mkdir -p {self.__target_dir}" )
      if 0 != result["code"]:
         return False

      result = self.execute( f"mkdir -p {self.__product_dir}" )
      if 0 != result["code"]:
         return False

      result = self.execute( f"mkdir -p {self.__deploy_dir}" )
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
            self.execute( f"file {artifact}", output = pfw.shell.eOutput.PTY )
         else:
            pfw.console.debug.error( f"artifact '{artifact}' does not exist" )
            result = False

      return result
   # def test



   def __get_config( self, keys ):
      return pfw.base.dict.get_value( self.__config, keys )
   # def __get_config



   def component_dir( self ):
      return self.__component_dir
   # def component_dir

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

   def execute( self, command, *argv, **kwargs ):
      kwargs["output"] = kwargs.get( "output", pfw.shell.eOutput.PTY )
      kwargs["cwd"] = kwargs.get( "cwd", self.__target_dir )
      kwargs["env"] = None # kwargs.get( "env", self.__environment )

      return pfw.shell.execute( f"{self.__export} {command}", *argv, **kwargs )
   # def execute
# class Builder
