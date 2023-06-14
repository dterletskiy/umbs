import os

import pfw.console
import pfw.archive
import pfw.shell

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )
# def get_instance



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__target = self.__config['config']
   # def __init__

   def config( self, **kwargs ):
      command = f""
      result = self.execute( command, print = False, collect = False )
      if 0 != result["code"]:
         return False

      return True
   # def config

   def build( self, **kwargs ):
      command = f"tools/bazel run --sandbox_debug {self.__target}_dist -- --dist_dir={self.__deploy_dir}"
      result = self.execute( command )
      if 0 != result["code"]:
         return False

      return True
   # def build

   def clean( self, **kwargs ):
      command = f"tools/bazel clean --expunge"
      result = self.execute( command )
      if 0 != result["code"]:
         return False

      return True
   # def clean
# class Builder
