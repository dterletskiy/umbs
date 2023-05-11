import os

import pfw.console
import pfw.shell
import pfw.linux.file

import umbs.base
import umbs.tools.base



def get_instance( config, **kwargs ):
   return Tool( config, **kwargs )
# def get_instance

def do_exec( tool ):
   if not tool.exec( ):
      pfw.console.debug.error( "exec error" )
      return False
   if not tool.test( ):
      pfw.console.debug.error( "test error" )
      return False

   return True
# def do_exec

def do_clean( tool ):
   if not tool.clean( ):
      pfw.console.debug.error( "clean error" )
      return False

   return True
# def do_clean



class Tool( umbs.tools.base.Tool ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "content" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      self.__content = self.__config[ "content" ]
   # def __init__

   def clean( self, **kwargs ):
      result = True
      for item in self.__content:
         op_result = pfw.shell.execute(
               f"rm {os.path.join( self.__target_dir, item['to'] )}",
               output = pfw.shell.eOutput.PTY,
               cwd = self.__target_dir
            )
         if 0 != op_result["code"]:
            result = False

      return result
   # def clean

   def exec( self, **kwargs ):
      result = True
      for item in self.__content:
         op_result = pfw.linux.file.copy(
               os.path.join( self.__root_dir, item["from"] ),
               os.path.join( self.__target_dir, item["to"] ),
               force = True
            )
         result = result and op_result

      return result
   # def exec
# class Tool
