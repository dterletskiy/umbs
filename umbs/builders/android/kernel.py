import os

import pfw.console
import pfw.archive
import pfw.shell

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )
# def get_instance

def do_build( builder ):
   if not builder.prepare( ):
      pfw.console.debug.error( "prepare error" )
      return False
   if not builder.config( ):
      pfw.console.debug.error( "config error" )
      return False
   if not builder.build( ):
      pfw.console.debug.error( "build error" )
      return False
   if not builder.test( ):
      pfw.console.debug.error( "test error" )
      return False

   return True
# def do_build

def do_clean( builder ):
   if not builder.clean( ):
      pfw.console.debug.error( "clean error" )
      return False

   return True
# def do_clean



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__target = self.__config['config']
   # def __init__

   def config( self, **kwargs ):
      command = f""
      result = pfw.shell.execute( command, cwd = self.__target_dir, print = False, collect = False )
      if 0 != result["code"]:
         return False

      return True
   # def config

   def build( self, **kwargs ):
      command = f"tools/bazel run --sandbox_debug {self.__target}_dist -- --dist_dir={self.__deploy_dir}"
      result = pfw.shell.execute( command, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      if 0 != result["code"]:
         return False

      return True
   # def build

   def clean( self, **kwargs ):
      command = f"tools/bazel clean --expunge"
      result = pfw.shell.execute( command, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      if 0 != result["code"]:
         return False

      return True
   # def clean
# class Builder
