import os
import re
import subprocess

import pfw.console
import pfw.shell
import pfw.size
import pfw.archive
import pfw.linux.image
import pfw.linux.fs
import pfw.linux.file
import pfw.linux.archive

import umbs.base
import umbs.builders.base



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )
# def get_instance



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      # Set "reuse" flag. This flag means that if image file with current name already exists
      # it will be used for further useage and build process in case if "reuse" flag is set to "true".
      # In cae if "reuse" flag is set to "false", new image file will be created always.
      self.__reuse = self.__config.get( "reuse", False )

      strict_fields = [ "file" ] if self.__reuse else [ "file", "size", "fs" ]
      for key in strict_fields:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in builder" )

      self.__file = os.path.join( self.__target_dir, self.__config["file"] )

      if not self.__reuse:
         if match := re.match( r'(\d+[.]?\d*)\s*(\w+)', self.__config["size"] ):
            if not pfw.size.text_to_size( match.group( 2 ) ):
               raise umbs.base.YamlFormatError( f"image size dimention error" )
            self.__size = pfw.size.Size( float( match.group( 1 ) ), pfw.size.text_to_size( match.group( 2 ) ) )
         else:
            raise umbs.base.YamlFormatError( f"image size format error" )

         self.__fs = pfw.linux.fs.builder( self.__config["fs"] )
         if not self.__fs:
            raise umbs.base.YamlFormatError( f"image fs format error" )
      else:
         if not os.path.exists( self.__file ):
            pfw.console.debug.warning( f"'reuse' flag is set to 'true' for not existing file '{self.__file}'" )


      self.__label = self.__config.get( "label", "NoLabel" )
      self.__content = self.__config.get( "content", [ ] )
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
      for item in self.__content:
         if "copy" == item["action"]:
            pfw.linux.file.copy(
                  os.path.join( self.__root_dir, item["from"] ),
                  os.path.join( self.__mount_point, item["to"] ),
                  sudo = True,
                  force = True
               )
         elif "extract" == item["action"]:
            pfw.linux.archive.unpack(
                  os.path.join( self.__root_dir, item["from"] ),
                  os.path.join( self.__mount_point, item["to"] ),
                  item["format"],
                  sudo = True
               )
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

      result = pfw.shell.execute( f"mv {self.__file} {self.__deploy_dir}", output = pfw.shell.eOutput.PTY )
      if 0 != result["code"]:
         return False

      return True
   # def deploy

   def clean( self, **kwargs ):
      result = pfw.shell.execute( f"rm -rf {' '.join( self.__artifacts )}", output = pfw.shell.eOutput.PTY )
      if 0 != result["code"]:
         return False

      return True
   # def clean



   def mount_point( self ):
      return self.__mount_point
   # def mount_point

   def __mount( self, **kwargs ):
      self.__mount_point = pfw.linux.image.mount( self.__file )
      # pfw.shell.execute( f"chown -R {os.geteuid( )}:{os.getegid( )} {self.__mount_point}", sudo = True, output = pfw.shell.eOutput.PTY )
   # def __mount

   def __umount( self, **kwargs ):
      pfw.linux.image.umount( self.__file )
   # def __umount
# class Builder
