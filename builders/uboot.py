import pfw.console
import pfw.archive
import pfw.shell



def get_builder( config, directory, **kwargs ):
   return UBoot( config, directory, **kwargs )

def do_build( builder ):
   builder.config( )
   builder.build( )



class UBoot:
   def __init__( self, config, directory, **kwargs ):
      self.__config = config
      self.__dir = directory

      self.__command = "make"
      # self.__command += f" O={self.__dir}"
      self.__command += f" -C {self.__dir}"
      self.__command += f" V=1"
      # self.__command += f" ARCH={self.__config['arch']}"
      # self.__command += f" -j{self.__config['cores']}"
      self.__command += f" CROSS_COMPILE={self.__config['compiler']}"
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
      command = self.__command
      targets = kwargs.get( "targets", self.__config['defconfig'] )

      pfw.shell.execute( command, targets, cwd = self.__dir, print = False, collect = False )
   # def config

   def build( self, **kwargs ):
      command = self.__command
      targets = kwargs.get( "targets", "all" )

      pfw.shell.execute( command, targets, output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def build

   def clean( self, **kwargs ):
      command = self.__command
      targets = kwargs.get( "targets", "clean distclean mrproper" )

      pfw.shell.execute( command, targets, output = pfw.shell.eOutput.PTY, cwd = self.__dir )
   # def clean

   def deploy( self, **kwargs ):
      pass
   # def deploy



   __config: dict = None
   __dir: dict = None
   __command: str = None
# class UBoot
