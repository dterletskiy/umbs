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

def do_build( builder ):
   builder.config( )
   builder.build( )
   builder.test( )

def do_clean( builder ):
   builder.clean( )



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "file", "size", "fs" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in builder" )


      if match := re.match( r'(\d+[.]?\d*)\s*(\w+)', self.__config["size"] ):
         if not pfw.size.text_to_size( match.group( 2 ) ):
            raise umbs.base.YamlFormatError( f"image size dimention error" )
         self.__size = pfw.size.Size( float( match.group( 1 ) ), pfw.size.text_to_size( match.group( 2 ) ) )
      else:
         raise umbs.base.YamlFormatError( f"image size format error" )

      self.__fs = pfw.linux.fs.builder( self.__config["fs"] )
      if not self.__fs:
         raise umbs.base.YamlFormatError( f"image fs format error" )

      self.__file = os.path.join( self.__target_dir, self.__config["file"] )
      self.__label = self.__config.get( "label", "NoLabel" )
      self.__content = self.__config.get( "content", [ ] )
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
      pfw.shell.execute( f"rm -rf {' '.join( self.__artifacts )}", output = pfw.shell.eOutput.PTY )
   # def clean
# class Builder
