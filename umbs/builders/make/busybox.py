import os

import pfw.console
import pfw.shell

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )
# def get_instance



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__targets = ' '.join( self.__config["targets"] ) if "targets" in self.__config else "all install"
      self.__defconfig = self.__config["defconfig"]
   # def __init__

   def config( self, **kwargs ):
      result = self.execute( self.build_command( ), self.__defconfig, print = False, collect = False )
      if 0 != result["code"]:
         return False

      return True
   # def config

   def build( self, **kwargs ):
      result = self.execute( self.build_command( ), self.__targets )
      if 0 != result["code"]:
         return False

      return True
   # def build

   def clean( self, **kwargs ):
      result = self.execute( self.build_command( ), "clean distclean mrproper" )
      if 0 != result["code"]:
         return False

      return True
   # def clean

   def build_command( self, **kwargs ):
      command = "make"
      command += f" O={self.__product_dir}"
      command += f" -C {self.__target_dir}"
      command += f" V=1"
      command += f" -j{str( self.__config['jobs'] )}" if "jobs" in self.__config else ""
      if all( key in self.__config for key in [ "arch", "compiler" ] ):
         command += f" ARCH={self.__config['arch']}"
         command += f" CROSS_COMPILE={self.__config['compiler']}"

      return command
   # def build_command
# class Builder
