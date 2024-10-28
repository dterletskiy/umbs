import os

import pfw.console
import pfw.shell
import pfw.base.function
import pfw.os.environment

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
            "source",
            self.__get_config( ["subdirs", "target"], "" )
         )
      # product_subdir <=> build code dir
      self.__product_dir = os.path.join(
            self.__component_dir,
            "product",
            self.__get_config( ["subdirs", "product"], "" )
         )
      # deploy_subdir <=> deploy code dir
      self.__deploy_dir = os.path.join(
            self.__component_dir,
            "install",
            self.__get_config( ["subdirs", "deploy"], "" )
         )

      self.__artifacts = [
            os.path.join( self.__deploy_dir, a ) for a in self.__get_config( "artifacts", [ ] ) if a
         ]
   # def __init__

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

   def artifacts( self ):
      return self.__artifacts
   # def artifacts
# class Actor
