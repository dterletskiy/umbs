import os

import pfw.console
import pfw.shell

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

      self.__command = "make"
      self.__command += f" -j{str( self.__config['jobs'] )}" if "jobs" in self.__config else ""
      if all( key in self.__config for key in [ "arch", "compiler" ] ):
         self.__command += f" XEN_TARGET_ARCH={self.__config['arch']}"
         self.__command += f" CROSS_COMPILE={self.__config['compiler']}"

      self.__targets = ' '.join( self.__config["targets"] ) if "targets" in self.__config else "dist dist-xen dist-tools dist-docs"
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def config( self, **kwargs ):
      command = "./configure"

      pfw.shell.execute( command, cwd = self.__target_dir, print = False, collect = False )
   # def config

   def build( self, **kwargs ):
      pfw.shell.execute( self.__command, self.__targets, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
   # def build

   def clean( self, **kwargs ):
      pfw.shell.execute( self.__command, "clean distclean mrproper", output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
   # def clean
# class Builder
