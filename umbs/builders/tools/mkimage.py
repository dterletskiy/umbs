import os

import pfw.console
import pfw.shell

import umbs.base



def get_builder( config, directory, **kwargs ):
   return Tool( config, directory, **kwargs )

def do_build( tool ):
   tool.build( )
   tool.test( )

def do_clean( tool ):
   tool.clean( )



class Tool:
   def __init__( self, config, directory, **kwargs ):
      self.__root_dir = kwargs.get( "root_dir", None )

      self.__config = config
      self.__dir = directory

      self.__artifacts = [ os.path.join( self.__dir, artifact ) for artifact in self.__config.get( "artifacts", [ ] ) ]

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

   def clean( self, **kwargs ):
      pfw.shell.execute( f"rm {self.__out}", output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def clean

   def build( self, **kwargs ):
      pfw.shell.execute( self.__command, output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def build

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
   __artifacts: list = [ ]

   __command: str = None
   __out: str = None
# class Tool
