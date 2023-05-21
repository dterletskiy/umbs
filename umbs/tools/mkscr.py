import os
import re

import pfw.console
import pfw.shell

import umbs.base
import umbs.tools.base



def get_instance( config, **kwargs ):
   return Tool( config, **kwargs )
# def get_instance



class Tool( umbs.tools.base.Tool ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in [ "source", "out" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in tool" )


      self.__source = os.path.join( self.__root_dir, self.__config["source"] )
      self.__out = os.path.join( self.__target_dir, self.__config["out"] )
   # def __init__

   def exec( self, **kwargs ):
      return self.__build_uboot_script( self.__source, self.__out )
   # def exec

   def clean( self, **kwargs ):
      result = pfw.shell.execute( f"rm {self.__out}", output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      return 0 == result["code"]
   # def clean

   # Function for building u-boot script from different u-boot scripts.
   # This smaller u-boot scripts are used for decomposition and more convenient usage.
   # There must be defined "main" u-boot script (mentioned in first parameter what uses "import" directive
   # inside what will be directly substituted during its processing by this function.
   # As a result complete u-boot script will be build and stored to the path mentioned in second parameter.
   def __build_uboot_script_lines( self, script_file_path: str ):
      pattern: str = r"^\s*import\s*\"(.*)\"\s*$"

      script_file_dir = os.path.dirname( script_file_path )

      try:
         script_file_h = open( script_file_path, "r" )
      except OSError:
         pfw.console.debug.error(  f"Could not open/read file: {script_file_path}" )
         return None

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
      result = pfw.shell.execute( f"mkdir -p {os.path.dirname( script_out_file )}", output = pfw.shell.eOutput.PTY, cwd = self.__target_dir )
      if 0 != result["code"]:
         return False

      code = self.__build_uboot_script_lines( script_in_file )
      if None == code:
         return False

      try:
         script_out_file_h = open( script_out_file, "w+" )
      except OSError:
         pfw.console.debug.error(  f"Could not open/read file: {script_out_file}" )
         return False

      try:
         script_out_file_h.write( code )
      except OSError:
         pfw.console.debug.error(  f"Could not write file: {script_out_file}" )
         return False

      script_out_file_h.close( )

      return True
   # def __build_uboot_script
# class Tool
