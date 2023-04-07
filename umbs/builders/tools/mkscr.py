import os
import re

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

      for key in [ "source", "out" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      self.__source = os.path.join( self.__root_dir, self.__config["source"] )
      self.__out = os.path.join( self.__dir, self.__config["out"] )
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
      self.__build_uboot_script( self.__source, self.__out )
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

   # Function for building u-boot script from different u-boot scripts.
   # This smaller u-boot scripts are used for decomposition and more convenient usage.
   # There must be defined "main" u-boot script (mentioned in first parameter what uses "import" directive
   # inside what will be directly substituted during its processing by this function.
   # As a result complete u-boot script will be build and stored to the path mentioned in second parameter.
   def __build_uboot_script_lines( self, script_file_path: str ):
      pattern: str = r"^\s*import\s*\"(.*)\"\s*$"

      script_file_dir = os.path.dirname( script_file_path )

      script_file_h = open( script_file_path, "r" )
      code: str = f"\n######################### Begin file '{script_file_path} #########################\n\n\n"
      for script_in_file_line in script_file_h:
         match = re.match( pattern, script_in_file_line )
         if match:
            import_file_name = match.group( 1 )
            import_file_path = os.path.join( script_file_dir, import_file_name )
            code += self.__build_uboot_script_lines( import_file_path )
         else:
            code += script_in_file_line
      code += f"\n#########################  End file '{script_file_path}  #########################\n\n\n"
      script_file_h.close( )

      return code
   # def __build_uboot_script_lines

   def __build_uboot_script( self, script_in_file: str, script_out_file: str ):
      pfw.shell.execute( f"mkdir -p {os.path.dirname( script_out_file )}", output = pfw.shell.eOutput.PTY, cwd = self.__dir )

      code = self.__build_uboot_script_lines( script_in_file )
      script_out_file_h = open( script_out_file, "w+" )
      script_out_file_h.write( code )
      script_out_file_h.close( )
   # def __build_uboot_script



   __config: dict = None
   __dir: str = None
   __root_dir: str = None
   __artifacts: list = [ ]

   __source: str = None
   __out: str = None
# class Tool
