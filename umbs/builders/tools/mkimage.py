import os

import pfw.console
import pfw.shell

import umbs.base
import umbs.builders.base



def get_builder( config, directory, **kwargs ):
   return Builder( config, directory, **kwargs )

def do_build( tool ):
   tool.build( )
   tool.test( )

def do_clean( tool ):
   tool.clean( )



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, directory, **kwargs ):
      super( ).__init__( config, directory, **kwargs )

      for key in [ "exe", "sources", "out" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )

      __exe = os.path.join( self.__root_dir, self.__config["exe"] )
      __arch = self.__config.get( "arch", None )
      __os = self.__config.get( "os", None )
      __img_type = self.__config.get( "img_type", None )
      __name = self.__config.get( "name", None )
      __load_addr = self.__config.get( "load_addr", None )
      __entry_point = self.__config.get( "entry_point", None )
      __compression = self.__config.get( "compression", None )

      __out = os.path.join( self.__dir, self.__config["out"] )

      __sources = self.__config["sources"]
      if isinstance( __sources, str ):
         __sources = [ __sources ]
      if not isinstance( __sources, list ) and not isinstance( __sources, tuple ):
         raise umbs.base.YamlFormatError( f"Filed 'sources' must be string or list" )
      if "multi" != __img_type and 1 < len( __sources ):
         raise umbs.base.YamlFormatError( f"image type could be only 'multi' for multiple source files" )
      for index, source in enumerate( __sources ):
         __sources[ index ] = os.path.join( self.__root_dir, source )
      __sources = ':'.join( __sources )

      self.__command = f"mkdir -p {os.path.dirname( __out )};"
      self.__command += f" {__exe}"
      self.__command += f" -A {__arch}" if __arch else ""
      self.__command += f" -O {__os}" if __os else ""
      self.__command += f" -C {__compression}" if __compression else ""
      self.__command += f" -T {__img_type}" if __img_type else ""
      self.__command += f" -a {__load_addr}" if __load_addr else ""
      self.__command += f" -e {__entry_point}" if __entry_point else ""
      self.__command += f" -n {__name}" if __name else ""
      self.__command += f" -d {__sources}"
      self.__command += f" {__out}"

      self.__out = __out
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def clean( self, **kwargs ):
      pfw.shell.execute( f"rm {self.__out}", output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def clean

   def build( self, **kwargs ):
      pfw.shell.execute( self.__command, output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def build
# class Builder
