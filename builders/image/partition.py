import os
import re
import subprocess

import pfw.console
import pfw.shell
import pfw.size
import pfw.linux.image
import pfw.linux.fs
import pfw.linux.file

import base



def get_builder( config, directory, **kwargs ):
   return Builder( config, directory, **kwargs )

def do_build( builder ):
   builder.config( )
   builder.build( )
   builder.test( )

def do_clean( builder ):
   builder.clean( )



class Builder:
   def __init__( self, config, directory, **kwargs ):
      self.__root_dir = kwargs.get( "root_dir", None )

      self.__config = config
      self.__dir = directory

      if "file" not in self.__config:
         raise base.YamlFormatError( f"Filed 'file' must be defined in builder" )
      if "size" not in self.__config:
         raise base.YamlFormatError( f"Filed 'size' must be defined in builder" )
      if "fs" not in self.__config:
         raise base.YamlFormatError( f"Filed 'fs' must be defined in builder" )


      if match := re.match( r'(\d+[.]?\d*)\s*(\w+)', self.__config["size"] ):
         if not pfw.size.text_to_size( match.group( 2 ) ):
            raise base.YamlFormatError( f"image size dimention error" )
         self.__size = pfw.size.Size( float( match.group( 1 ) ), pfw.size.text_to_size( match.group( 2 ) ) )
      else:
         raise base.YamlFormatError( f"image size format error" )

      self.__fs = pfw.linux.fs.builder( self.__config["fs"] )
      if not self.__fs:
         raise base.YamlFormatError( f"image fs format error" )

      self.__file = os.path.join( self.__dir, self.__config["file"] )
      self.__label = self.__config.get( "label", "NoLabel" )
      self.__content = self.__config.get( "content", [ ] )
      self.__artifacts = [ os.path.join( self.__dir, artifact ) for artifact in self.__config.get( "artifacts", [ ] ) ]
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __setattr__( self, attr, value ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) ]
      if attr in attr_list:
         self.__dict__[ attr ] = value
         return
      raise AttributeError
   # def __setattr__

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

   def config( self, **kwargs ):
      pass
   # def config

   def build( self, **kwargs ):
      pfw.linux.image.create( self.__file, self.__size )
      pfw.linux.image.format( self.__file, self.__fs, label = self.__label )
      mount_point = pfw.linux.image.mount( self.__file )

      for item in self.__content:
         pfw.linux.file.copy(
               os.path.join( self.__root_dir, item["from"] ),
               os.path.join( mount_point, item["to"] ),
               sudo = True, force = True
            )

      pfw.linux.image.umount( self.__file )

      def processor( **kwargs ):
         kw_mount_point = kwargs.get( "mount_point", None )

         if kw_mount_point:
            subprocess.Popen(['xdg-open', kw_mount_point])
            pfw.console.debug.promt( )
      # def processor
      pfw.linux.image.map( self.__file, processor = processor )
   # def build

   def clean( self, **kwargs ):
      pass
   # def clean

   def deploy( self, **kwargs ):
      pass
   # def deploy

   def test( self, **kwargs ):
      result: bool = True

      for artifact in self.__artifacts:
         if os.path.exists( artifact ):
            pfw.console.debug.ok( f"artifact '{artifact}' exists" )
         else:
            pfw.console.debug.error( f"artifact '{artifact}' does not exist" )
            result = False

      return result
   # def test



   __config: dict = None
   __dir: str = None
   __root_dir: str = None
   __artifacts: list = [ ]

   __size: pfw.size.Size = None
   __fs: pfw.linux.fs = None
   __label: str = None
   __file: str = None
   __content: list = None
# class Builder
