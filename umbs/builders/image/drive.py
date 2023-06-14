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
import umbs.builders.base



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )
# def get_instance



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

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

      self.__file = os.path.join( self.__target_dir, self.__config["file"] )
      self.__partitions = self.__config.get( "partitions", [ ] )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def build( self, **kwargs ):
      self.__build( **kwargs )

      return True
   # def build

   def __build( self, **kwargs ):
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
   # def __build

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
# class Builder
