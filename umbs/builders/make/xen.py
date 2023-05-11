import os

import pfw.console
import pfw.shell

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )
# def get_instance

def do_build( builder ):
   if not builder.prepare( ):
      pfw.console.debug.error( "prepare error" )
      return False
   if not builder.config( ):
      pfw.console.debug.error( "config error" )
      return False
   if not builder.build( ):
      pfw.console.debug.error( "build error" )
      return False
   if not builder.test( ):
      pfw.console.debug.error( "test error" )
      return False

   return True
# def do_build

def do_clean( builder ):
   if not builder.clean( ):
      pfw.console.debug.error( "clean error" )
      return False

   return True
# def do_clean



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__targets = ' '.join( self.__config["targets"] ) if "targets" in self.__config else "dist dist-xen dist-tools dist-docs"
   # def __init__

   def config( self, **kwargs ):
      command = f"./configure"
      # command += f" --prefix={self.__product_dir}"
      # command += f" --exec_prefix={self.__deploy_dir}"

      result = pfw.shell.execute( command, cwd = self.__target_dir, print = False, collect = False )
      if 0 != result["code"]:
         return False

      return True
   # def config

   def build( self, **kwargs ):
      result = pfw.shell.execute( self.build_command( ), self.__targets, output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      if 0 != result["code"]:
         return False

      result = pfw.shell.execute( f"cp -r dist/* {self.__deploy_dir}", output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      if 0 != result["code"]:
         return False

      return True
   # def build

   def clean( self, **kwargs ):
      result = pfw.shell.execute( self.build_command( ), "clean distclean mrproper", output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      if 0 != result["code"]:
         return False

      return True
   # def clean

   def build_command( self, **kwargs ):
      # command = "make install"
      # command += f" prefix={self.__product_dir}"
      # command += f" exec_prefix={self.__deploy_dir}"
      # command += f" O={self.__product_dir}"
      # command += f" -C {self.__target_dir}"
      command = "make"
      command += f" -j{str( self.__config['jobs'] )}" if "jobs" in self.__config else ""
      if all( key in self.__config for key in [ "arch", "compiler" ] ):
         command += f" XEN_TARGET_ARCH={self.__config['arch']}"
         command += f" CROSS_COMPILE={self.__config['compiler']}"

      return command
   # def build_command
# class Builder
