import os
import re
import subprocess

import pfw.console
import pfw.shell
import pfw.size
import pfw.linux.image
import pfw.linux.fs
import pfw.linux.file

import umbs.base



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

      for key in [ "file" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in builder" )


      if "size" in self.__config:
         if match := re.match( r'(\d+[.]?\d*)\s*(\w+)', self.__config["size"] ):
            if not pfw.size.text_to_size( match.group( 2 ) ):
               raise umbs.base.YamlFormatError( f"image size dimention error" )
            self.__size = pfw.size.Size( float( match.group( 1 ) ), pfw.size.text_to_size( match.group( 2 ) ) )
         else:
            raise umbs.base.YamlFormatError( f"image size format error" )

      self.__file = os.path.join( self.__dir, self.__config["file"] )
      self.__partitions = self.__config.get( "partitions", [ ] )
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
      partitions = [ ]
      for partition in self.__partitions:
         if "file" in partition:
            partitions.append(
                  pfw.linux.image.Partition(
                        clone_from = os.path.join( self.__root_dir, partition["file"] ),
                        label = partition.get( "label", None )
                     )
               )
         elif "size" in partition and "fs" in partition:
            size = None
            if match := re.match( r'(\d+[.]?\d*)\s*(\w+)', partition["size"] ):
               if not pfw.size.text_to_size( match.group( 2 ) ):
                  raise umbs.base.YamlFormatError( f"aprtition size dimention error" )
               size = pfw.size.Size( float( match.group( 1 ) ), pfw.size.text_to_size( match.group( 2 ) ) )
            else:
               raise umbs.base.YamlFormatError( f"partition size format error" )

            fs = pfw.linux.fs.builder( partition["fs"] )
            if not fs:
               raise umbs.base.YamlFormatError( f"partition fs format error" )

            partitions.append(
                  pfw.linux.image.Partition(
                        size = size,
                        fs = fs,
                        label = partition["label"]
                     )
               )
         else:
            raise umbs.base.YamlFormatError( f"Filed 'file' or 'size' and 'fs' must be defined in partition definition" )

      device = pfw.linux.image.Device( partitions = partitions )
      pfw.linux.image.create( self.__file, device.size( ) )
      pfw.linux.image.init_device( self.__file, device )

      def processor( **kwargs ):
         kw_mount_point = kwargs.get( "mount_point", None )

         if kw_mount_point:
            subprocess.Popen(['xdg-open', kw_mount_point])
            pfw.console.debug.promt( )
      # def processor
      pfw.linux.image.map( self.__file, processor = processor )
   # def build

   def clean( self, **kwargs ):
      pfw.shell.execute( f"rm -rf {' '.join( self.__artifacts )}", output = pfw.shell.eOutput.PTY )
   # def clean

   def deploy( self, **kwargs ):
      pass
   # def deploy

   def test( self, **kwargs ):
      result: bool = True

      for artifact in self.__artifacts:
         if os.path.exists( artifact ):
            pfw.console.debug.ok( f"artifact '{artifact}' exists" )
            pfw.shell.execute( f"file {artifact}", output = pfw.shell.eOutput.PTY )
         else:
            pfw.console.debug.error( f"artifact '{artifact}' does not exist" )
            result = False

      return result
   # def test



   __config: dict = None
   __dir: str = None
   __root_dir: str = None
   __partitions: list = None
   __artifacts: list = None

   __size: pfw.size.Size = None
   __file: str = None
# class Builder
