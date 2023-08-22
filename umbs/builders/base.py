import os

import pfw.console
import pfw.shell
import pfw.base.function
import pfw.os.environment

import umbs.base
import umbs.actors.base



class Actor( umbs.actors.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__(
            config = config,
            exec = [
                  pfw.base.function.Holder( self.prepare ),
                  pfw.base.function.Holder( self.config ),
                  pfw.base.function.Holder( self.build ),
                  pfw.base.function.Holder( self.deploy ),
                  pfw.base.function.Holder( self.test )
               ],
            clean = [
                  pfw.base.function.Holder( self.clean )
               ],
            **kwargs
         )

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
   # def __init__

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
# class Actor
