import os

import pfw.console
import pfw.shell

import umbs.base
import umbs.tools.base



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( umbs.tools.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "sources", "out" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )

      __exe = "mkimage"
      if "exe" in self.__config:
         __exe = os.path.join( self.__root_dir, self.__config["exe"] )
      __arch = self.__config.get( "arch", None )
      __os = self.__config.get( "os", None )
      __img_type = self.__config.get( "img_type", None )
      __name = self.__config.get( "name", None )
      __load_addr = self.__config.get( "load_addr", None )
      __entry_point = self.__config.get( "entry_point", None )
      __compression = self.__config.get( "compression", None )

      __out = os.path.join( self.__target_dir, self.__config["out"] )

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

   def exec( self, **kwargs ):
      result = pfw.shell.execute( self.__command, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      return 0 == result["code"]
   # def exec

   def clean( self, **kwargs ):
      result = pfw.shell.execute( f"rm {self.__out}", output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      return 0 == result["code"]
   # def clean
# class Actor
