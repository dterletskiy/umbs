#!/usr/bin/python

import copy
import re
import os
import yaml

import pfw.console
import pfw.base.str
import pfw.base.dict

import umbs.configuration



class YamlFormatError( Exception ):
   def __init__( self, message ):
      self.message = message
      super( ).__init__( self.message )

   def __str__( self ):
      pfw.console.debug.error( f"{self.__class__}: {self.message}" )
# class YamlFormatError

class ConfigurationFormatError( Exception ):
   def __init__( self, message ):
      self.message = message
      super( ).__init__( self.message )

   def __str__( self ):
      pfw.console.debug.error( f"{self.__class__}: {self.message}" )
# class ConfigurationFormatError



class Config:
   def __init__( self, file: str, **kwargs ):
      def read_file( file, spaces: str = "" ):
         pattern: str = r"^(\s*)include:\s*\"(.*)\"\s*$"

         lines: str = ""
         file_dir = os.path.dirname( file )

         yaml_fd = open( file, "r" )

         for line in yaml_fd:
            match = re.match( pattern, line )
            if match:
               import_file_name = match.group( 2 )
               import_file_path = os.path.join( file_dir, import_file_name )
               lines += read_file( import_file_path, match.group( 1 ) )
            else:
               lines += spaces + line

         yaml_fd.close( )
         return lines
      # def read_file

      yaml_lines = read_file( file )
      yaml_file = "./.gen/umbs.yaml"
      yaml_h = open( yaml_file, "w" )
      yaml_h.write( yaml_lines )
      yaml_h.close( )
      yaml_data = yaml.load( yaml_lines, Loader = yaml.SafeLoader )
      # yaml_stream = yaml.compose( yaml_fd )

      # Read "variables" section from yaml file
      self.__variables = yaml_data.get( "variables", { } )

      # Override some fields according to "config" file or command line
      for name in umbs.configuration.names( ):
         if not name.startswith( "YAML." ):
            continue

         replace_name = name.removeprefix( "YAML." )
         replace_value = umbs.configuration.value( name )
         self.set_variable( replace_name, replace_value )

      # Substitute valiables' values
      self.__process_yaml_data( self.__variables )

      # Test critical variables
      if None == self.get_variable( "DIRECTORIES.ROOT" ):
         raise ConfigurationFormatError(
               "Root directory must be defined in command line, confiruration file or in yaml file as 'DIRECTORIES.ROOT'"
            )

      # Read "components" section from yaml file
      self.__components = yaml_data.get( "components", { } )
      self.__process_yaml_data( self.__components )

      # Read "tools" section from yaml file
      self.__tools = yaml_data.get( "tools", { } )
      self.__process_yaml_data( self.__tools )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def info( self, **kwargs ):
      kw_tabs = kwargs.get( "tabs", 0 )
      kw_msg = kwargs.get( "msg", "" )
      pfw.console.debug.info( f"{kw_msg} (type {self.__class__.__name__}):", tabs = ( kw_tabs + 0 ) )
      pfw.console.debug.info( pfw.base.str.to_string( self.__variables ) )
      pfw.console.debug.info( pfw.base.str.to_string( self.__components ) )
      pfw.console.debug.info( pfw.base.str.to_string( self.__tools ) )
   # def info



   def get_variable( self, variable, default_value = None ):
      return pfw.base.dict.get_value( self.__variables, variable, default_value )
   # def get_variable

   def get_variables( self ):
      return self.__variables
   # def get_variables

   def set_variable( self, variable, value ):
      pfw.base.dict.set_value( self.__variables, variable, value )
   # def set_variable

   def get_component( self, name: str ):
      return self.__components[ name ]
   # def get_component

   def get_components( self ):
      return self.__components
   # def get_components

   def get_tool( self, name: str ):
      return self.__tools[ name ]
   # def get_tool

   def get_tools( self ):
      return self.__tools
   # def get_tools



   class AV:
      def __init__( self, a, v ):
         self.address = copy.deepcopy( a )
         self.value = copy.deepcopy( v )
      # def __init__

      def __del__( self ):
         pass
      # def __del__

      address: list = [ ]
      value = None
   # class AV

   def __replace( self, value ):
      # pfw.console.debug.trace( f"processing value: '{value}'" ) # @TDA: debug

      if not isinstance( value, str ):
         pfw.console.debug.warning( f"ERROR: '{value}' is not a string, it is {type( value )}" )
         return ( False, value )

      replaced: bool = False
      if findall := re.findall( r'\$\{(.+?)\}', value ):
         # pfw.console.debug.trace( f"findall: '{findall}'" ) # @TDA: debug
         for item in findall:
            variable = self.get_variable( item )
            # pfw.console.debug.trace( f"{item} -> {variable} ({type(variable)})" ) # @TDA: debug
            if isinstance( variable, str ) or isinstance( variable, int ) or isinstance( variable, float ):
               value = value.replace( "${" + item + "}", str(variable) )
            elif isinstance( variable, list ) or isinstance( variable, tuple ) or isinstance( variable, dict ):
               if value == "${" + f"{item}" + "}":
                  value = variable
               else:
                  pfw.console.debug.error( "can substitute only single variable without any other characters by list, tuple or map" )
                  raise YamlFormatError( f"Wrong yaml format error for substitutuion variable '{item}'" )

         if isinstance( value, str ):
            value = self.__replace( value )[1]

         replaced = True

      return ( replaced, value )
   # def __replace

   def __walk( self, iterable, address: list, value_processor = None ):
      # pfw.console.debug.info( f"-> address = {address}" ) # @TDA: debug

      for_adaptation: list = [ ]
      if isinstance( iterable, dict ):
         for key, value in iterable.items( ):
            new_address = address
            new_address.append( key )
            for_adaptation.extend( self.__walk( value, new_address, value_processor ) )
            del address[-1]
      elif isinstance( iterable, list ) or isinstance( iterable, tuple ):
         for index, item in enumerate( iterable ):
            new_address = address
            new_address.append( index )
            for_adaptation.extend( self.__walk( item, new_address, value_processor ) )
            del address[-1]
      elif isinstance( iterable, str ):
         ( replaced, new_value ) = value_processor( iterable )
         if replaced:
            # print( f"address = {address}" ) # @TDA: debug
            # print( f"old_value = {iterable}" ) # @TDA: debug
            # print( f"new_value = {new_value}" ) # @TDA: debug
            for_adaptation.append( Config.AV( address, new_value ) )
      else:
         pass

      # pfw.console.debug.info( f"<- address = {address}" ) # @TDA: debug

      return for_adaptation
   # def __walk

   def __process_yaml_data( self, yaml_data ):
      for item in self.__walk( yaml_data, [ ], self.__replace ):
         pfw.base.dict.set_value_by_list_of_keys( yaml_data, item.address, item.value )
   # def __process_yaml_data



   __variables: dict = { }
   __components: dict = { }
   __tools: dict = { }
# class Config

