import os

import pfw.console
import pfw.archive
import pfw.shell



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

      self.__artifacts = [ os.path.join( self.__dir, artifact ) for artifact in self.__config.get( "artifacts", [ ] ) ]

      self.__command = "make"
      # self.__command += f" O={self.__dir}"
      self.__command += f" -C {self.__dir}"
      self.__command += f" V=1"
      self.__command += f" -j{str( self.__config['jobs'] )}" if "jobs" in self.__config else ""
      if all( key in self.__config for key in ( "arch", "compiler" ) ):
         self.__command += f" ARCH={self.__config['arch']}"
         self.__command += f" CROSS_COMPILE={self.__config['compiler']}"

      self.__targets = ' '.join( self.__config["targets"] ) if "targets" in self.__config else "all"

      self.__defconfig = self.__config["defconfig"]
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
      command = "./configure"
      # parameters = "--enable-gtk --enable-kvm --static --disable-system --enable-linux-user --enable-user"
      parameters = ""

      pfw.shell.execute( command, parameters, cwd = self.__dir, print = False, collect = False )
   # def config

   def build( self, **kwargs ):
      pfw.shell.execute( self.__command, self.__targets, output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def build

   def clean( self, **kwargs ):
      pfw.shell.execute( self.__command, "clean distclean mrproper", output = pfw.shell.eOutput.PTY, cwd = self.__dir )
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

   __command: str = None
# class Builder
