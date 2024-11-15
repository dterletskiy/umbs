import importlib
import os
import re

import pfw.console
import pfw.shell

import umbs.actors.types
module_builder_base = importlib.import_module( f"{umbs.actors.types.eType.BUILDER}.base", __package__ )



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( module_builder_base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      strict_fields = [ "target" ]
      for key in strict_fields:
         if key not in self.__config:
            raise pfw.base.yaml.YamlFormatError( f"Filed '{key}' must be defined in builder" )

      self.__target = self.__get_config( "target", None )
      self.__layers = [ os.path.join( self.__target_dir, layer ) for layer in self.__get_config( "layers", [ ] ) ]
      self.__bblayer_conf = os.path.join( self.__product_dir, "conf/bblayers.conf" )
      self.__local_conf = os.path.join( self.__product_dir, "conf/local.conf" )
   # def __init__

   def config( self, **kwargs ):
      # command = f"bitbake-layers add-layer {self.__layers}"
      # return 0 == self.__execute( command )["code"]

      if 0 != self.__execute( f"bitbake-layers show-layers" )["code"]:
         return False

      with open( self.__bblayer_conf, "r" ) as file:
         content = file.read( )

      layers = ' \\\n  '.join( self.__layers )
      pattern_search = r'BBLAYERS\s*\?=\s*"(.*?)"'
      pattern_replace = f'BBLAYERS ?= " \\\n  {layers} \\\n  "'
      content = re.sub( pattern_search, pattern_replace, content, flags = re.DOTALL )

      with open( self.__bblayer_conf, "w" ) as file:
         file.write( content )

      if 0 != self.__execute( f"bitbake-layers show-layers" )["code"]:
         return False

      return True
   # def config

   def build( self, **kwargs ):
      command = f"bitbake"
      command += f" --verbose"
      command += f" {self.__target}"
      return 0 == self.__execute( command )["code"]
   # def build

   def deploy( self, **kwargs ):
      artifacts = [
         ]

      deploy_result: bool = True
      for artifact in artifacts:
         result = pfw.shell.execute(
               f"cp --parents {artifact} {self.__deploy_dir}",
               cwd = self.__product_dir
            )
         if 0 != result["code"]:
            deploy_result = False

      return True
   # def deploy

   def clean( self, **kwargs ):
      return True
   # def clean

   def __execute( self, command ):
      if not command:
         return False

      return self.execute(
            f"source poky/oe-init-build-env {self.__product_dir} && {command}"
            , cwd = self.__target_dir
            , print = False
            , collect = False
         )
   # def __execute
# class Actor
