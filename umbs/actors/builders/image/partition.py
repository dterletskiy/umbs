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

      # Set "reuse" flag. This flag means that if image file with current name already exists
      # it will be used for further useage and build process in case if "reuse" flag is set to "true".
      # In cae if "reuse" flag is set to "false", new image file will be created always.
      self.__reuse = self.__get_config( "reuse", False )

      strict_fields = [ "file" ] if self.__reuse else [ "file", "size", "fs" ]
      for key in strict_fields:
         if key not in self.__config:
            raise pfw.base.yaml.YamlFormatError( f"Filed '{key}' must be defined in builder" )

      self.__file = os.path.join( self.__target_dir, self.__get_config( "file" ) )

      if not self.__reuse:
         self.__size = self.__get_config( "size", None )
         if not self.__size:
            raise pfw.base.yaml.YamlFormatError( f"image size must be defined" )

         self.__size = umbs.utils.string_to_size( self.__size )
         if None == self.__size:
            raise pfw.base.yaml.YamlFormatError( f"image size format error" )

         self.__fs = pfw.linux.fs.builder( self.__get_config( "fs" ) )
         if not self.__fs:
            raise pfw.base.yaml.YamlFormatError( f"image fs format error" )
      else:
         if not os.path.exists( self.__file ):
            pfw.console.debug.warning( f"'reuse' flag is set to 'true' for not existing file '{self.__file}'" )



      self.__mount_point = tempfile.mkdtemp( prefix = "mp_" )

      self.__label = self.__get_config( "label", "NoLabel" )
      self.__content = self.__get_config( "content", [ ] )
      for item in self.__content:
         if os.path.isabs( item["to"] ):
            raise pfw.base.yaml.YamlFormatError(
               f"Destination path '{item['to']}' must be relative to mount point '{self.__mount_point}'"
            )

         item["from"] = os.path.join( self.__component_dir, item["from"] )
         item["to"] = os.path.join( self.__mount_point, item["to"] )
   # def __init__

   def build( self, **kwargs ):
      self.__create( **kwargs )
      self.__mount( **kwargs )
      self.__build( **kwargs )
      self.__umount( **kwargs )
      self.__finalize( **kwargs )

      return True
   # def build

   def __create( self, **kwargs ):
      if False == self.__reuse:
         pfw.linux.image.create( self.__file, self.__size, force = not self.__reuse )
         pfw.linux.image.format( self.__file, self.__fs, label = self.__label )
   # def __create

   def __build( self, **kwargs ):
      result = True
      for item in self.__content:
         result = result and pfw.linux.file.copy( item["from"], item["to"], force = True, sudo = True )

      return result
   # def __build

   def __finalize( self, **kwargs ):
      def processor( **kwargs ):
         kw_mount_point = kwargs.get( "mount_point", None )

         if kw_mount_point:
            subprocess.Popen(['xdg-open', kw_mount_point])
            pfw.console.debug.promt( )
      # def processor
      pfw.linux.image.map( self.__file, processor = processor )
   # def __finalize

   def deploy( self, **kwargs ):
      if self.__target_dir == self.__deploy_dir:
         return True

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



   def mount_point( self ):
      return self.__mount_point
   # def mount_point

   def __mount( self, **kwargs ):
      self.__mount_point = pfw.linux.image.mount( self.__file, mount_point = self.__mount_point )
      # self.execute( f"chown -R {os.geteuid( )}:{os.getegid( )} {self.__mount_point}", sudo = True )
   # def __mount

   def __umount( self, **kwargs ):
      pfw.linux.image.umount( self.__file )
   # def __umount
# class Actor
