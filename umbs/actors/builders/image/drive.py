import importlib
import os
import re
import tempfile
import subprocess

import pfw.console
import pfw.shell
import pfw.size
import pfw.base.yaml
import pfw.linux.image
import pfw.linux.fs
import pfw.linux.file

import umbs.utils

import umbs.actors.types
module_builder_base = importlib.import_module( f"{umbs.actors.types.eType.BUILDER}.base", __package__ )



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( module_builder_base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "file" ]:
         if key not in self.__config:
            raise pfw.base.yaml.YamlFormatError( f"Filed '{key}' must be defined in builder" )
            

      self.__file = os.path.join( self.__target_dir, self.__get_config( "file" ) )

      partitions = [ ]
      for partition in self.__get_config( "partitions", [ ] ):
         label = partition.get( "label", None )

         size = partition.get( "size", None )
         if size:
            size = umbs.utils.string_to_size( size )
            if not size:
               raise pfw.base.yaml.YamlFormatError( f"image size format error" )

         fs = partition.get( "fs", None )
         if fs:
            fs = pfw.linux.fs.builder( fs )
            if not fs:
               raise pfw.base.yaml.YamlFormatError( f"image fs format error" )

         file = partition.get( "file", None )

         partitions.append(
               pfw.linux.image.Partition(
                  size = size,
                  fs = fs,
                  label = label,
                  clone_from = file,
                  bootable = partition.get( "bootable", False ),
                  esp = partition.get( "esp", False )
               )
            )
      self.__device = pfw.linux.image.Device( partitions = partitions )


      self.__size = self.__get_config( "size", None )
      if self.__size:
         self.__size = umbs.utils.string_to_size( self.__size )
         if None == self.__size:
            raise pfw.base.yaml.YamlFormatError( f"image size format error" )
      else:
         self.__size = self.__device.size( )
   # def __init__

   def build( self, **kwargs ):
      pfw.linux.image.create( self.__file, self.__size )
      pfw.linux.image.init_device( self.__file, self.__device )

      return True
   # def build

   def deploy( self, **kwargs ):
      result = self.execute( f"mv {self.__file} {self.__deploy_dir}" )
      if 0 != result["code"]:
         return False

      return True
   # def deploy

   def clean( self, **kwargs ):
      result = self.execute( f"rm -rf {' '.join( self.__artifacts )}" )
      if 0 != result["code"]:
         return False

      return True
   # def clean
# class Actor
