import os
import sys
import copy
import re
import getopt
import argparse



class ConfigurationData:
   def __init__( self, name: str, required: bool, destination: str ):
      self.__name = copy.deepcopy( name )
      self.__required = copy.deepcopy( required )
      self.__description = copy.deepcopy( destination )
      self.__values = [ ]
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

   def __gt__( self, other ):
      return self.__name > other.__name
   # def __gt__

   def __lt__( self, other ):
      return self.__name < other.__name
   # def __lt__

   def __eq__( self, other ):
      return self.__name == other.__name if None != other else False
   # def __eq__

   def info( self, **kwargs ):
      print( self.__class__.__name__, ":" )
      print( "name:         \'", self.__name, "\'" )
      print( "values:       \'", self.__values, "\'" )
      print( "required:     \'", self.__required, "\'" )
      print( "description:  \'", self.__description, "\'" )
   # def info



   # Get name of variable
   def get_name( self ):
      return self.__name
   # def get_name

   # Get index-th value of variable
   def get_value( self, index: int = 0 ):
      return self.__values[ index ] if index < len( self.__values ) else None
   # def get_value

   # Get all values of variable
   def get_values( self ):
      return self.__values
   # def get_values

   def set_value( self, value ):
      self.set_value_single( value )
   # def set_value

   def set_value_single( self, value ):
      self.__values.append( value )
   # def set_value_single

   # Set single value or list of values of variable
   # In fact this operation adds new value/values to existing value list of variable
   def set_value_ext( self, value ):
      if None == value:
         return

      values_to_add: list = [ ]
      if isinstance( value, list ) or isinstance( value, tuple ):
         values_to_add = value
      elif isinstance( value, dict ) or isinstance( value, set ):
         return
      else:
         values_to_add = [ value ]

      self.__values.extend( values_to_add )
   # def set_value_ext

   # Clear all values of variable
   def reset_value( self, name: str, value = None ):
      self.__values.clear( )

      if None == value:
         self.__values.append( value )
   # def reset_value

   # Test if value/values exists in list of values of variable
   def test_value( self, value ):
      if None == value:
         return False

      values_to_test: list = [ ]
      if isinstance( value, list ) or isinstance( value, tuple ):
         values_to_test = value
      elif isinstance( value, dict ):
         return
      else:
         values_to_test = [ value ]

      for value_to_test in values_to_test:
         if not ( value_to_test in self.__values ):
            return False

      return True
   # def test_value

   def get_required( self ):
      return self.__required
   # def get_required

   def get_description( self ):
      return self.__description
   # def get_description

   def is_satisfy( self ):
      result: bool = 0 < len( self.__values ) if True == self.__required else True

      if False == result:
         print( "configuration variable '%s' is not defined in command line paramenters and configuration file" % ( self.__name ) )
         print( "configuration variable '%s': '%s'" % ( self.__name, self.__description ) )

      return result
   # def is_satisfy



   __name: str = None
   __values: list = [ ]
   __required: bool = False
   __description: str = None
# class ConfigurationData



class ConfigurationContainer:
   def __init__( self, data_list: list = [ ], **kwargs ):
      self.__list = copy.deepcopy( data_list )
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
      print( self.__class__.__name__, ":" )
      for data in self.__list:
         data.info( )
   # def info



   def set_data( self, name: str, data: ConfigurationData ):
      self.__list.append( data )
   # def set_data

   def get_data( self, name: str ):
      for data in self.__list:
         if data.get_name( ) == name:
            return data

      return None
   # def get_data

   def get_data_list( self ):
      return self.__list
   # def get_data_list

   def get_names( self ):
      return [ i.get_name( ) for i in self.__list ]
   # def get_names

   def test( self, name: str ):
      return None != self.get_data( name )
   # def test

   def delete_data( self, name: str ):
      for index in range( len( self.__list ) ):
         if self.__list[ index ].get_name( ) == name:
            del self.__list[ index ]
   # def delete_data

   def set_value( self, name: str, value ):
      data = self.get_data( name )
      if None == data:
         data = ConfigurationData( name, False, "" )
         self.__list.append( data )

      data.set_value( value )
   # def set_value

   def get_values( self, name: str ):
      data = self.get_data( name )
      return data.get_values( ) if None != data else [ ]
   # def get_values

   def get_value( self, name: str, index: int = 0 ):
      data = self.get_data( name )
      return data.get_value( index ) if None != data else None
   # def get_value

   def get_description( self, name: str ):
      data = self.get_data( name )
      return data.get_description( ) if None != data else None
   # def get_description

   def get_required( self, name: str ):
      data = self.get_data( name )
      return data.get_required( ) if None != data else None
   # def get_required

   def is_complete( self ):
      for data in self.__list:
         if False == data.is_satisfy( ):
            return False

      return True
   # def is_complete



   __list: list = [ ]
# class ConfigurationContainer



def add_config( app_data, name, value ):
   app_data.set_value( name, value )

   for key in [ "pfw" ]:
      if key == name:
         app_data.set_value( "include", value )
# def add_config



def process_cmdline( app_data, argv ):
   print( "Number of arguments:", len(sys.argv) )
   print( "Argument List:", str(sys.argv) )

   parser = argparse.ArgumentParser( description = 'App description' )

   parser.add_argument( "--version", action = "version", version = '%(prog)s 2.0' )

   parser.add_argument( "--config", dest = "config", type = str, action = "append", required = False, help = app_data.get_description( "config" ) )
   parser.add_argument( "--yaml_config", dest = "yaml_config", type = str, action = "store", required = False, help = app_data.get_description( "yaml_config" ) )
   parser.add_argument( "--root_dir", dest = "root_dir", type = str, action = "store", required = False, help = app_data.get_description( "root_dir" ) )

   parser.add_argument( "--include", dest = "include", type = str, action = "append", required = False, help = app_data.get_description( "include" ) )
   parser.add_argument( "--pfw", dest = "pfw", type = str, action = "append", required = False, help = app_data.get_description( "pfw" ) )

   parser.add_argument( "--project", dest = "project", type = str, action = "store", required = False, default = "*", help = app_data.get_description( "project" ) )
   parser.add_argument( "--action", dest = "action", type = str, action = "store", required = False, default = "*", help = app_data.get_description( "action" ) )

   parser.add_argument( "--container", dest = "container", type = str, action = "store", required = False, default = None, help = app_data.get_description( "container" ) )

   # parser.print_help( )
   try:
      argument = parser.parse_args( )
   except argparse.ArgumentError:
      print( 'Catching an ArgumentError' )

   for key, value in argument.__dict__.items( ):
      if None == value:
         continue

      if isinstance( value, list ) or isinstance( value, tuple ):
         for item in value:
            add_config( app_data, key, item )
      else:
         add_config( app_data, key, value )
# def process_cmdline



def process_config_file( app_data ):
   pattern: str = r"^\s*(.*)\s*:\s*(.*)\s*$"

   config_files = app_data.get_values( "config" )
   print( f"Processing config files: {config_files}" )
   for config_file in config_files:
      print( f"Processing config file: '{config_file}'" )
      config_file_h = open( config_file, "r" )
      for line in config_file_h:
         match = re.match( pattern, line )
         if match:
            add_config( app_data, match.group( 1 ), match.group( 2 ) )
      config_file_h.close( )
      print( f"Processed config file: '{config_file}'" )
   print( f"Processed config files: {config_files}" )
# def process_config_file



def process_configuration( app_data, argv ):
   process_cmdline( app_data, argv )
   process_config_file( app_data )
   # app_data.info( )
   if False == app_data.is_complete( ):
      sys.exit( 1 )

   for path in reversed( app_data.get_values( "include" ) ):
      sys.path.insert( 0, path )
# def process_configuration



config: ConfigurationContainer = ConfigurationContainer(
      [
         ConfigurationData( "config"            , True  , "Path to configuration file" ),
         ConfigurationData( "yaml_config"       , True  , "Path to yaml project configuration file" ),
         ConfigurationData( "root_dir"          , False , "Path to project root directory" ),
         ConfigurationData( "include"           , False , "Additional directory to search import packages" ),
         ConfigurationData( "pfw"               , True  , "Python Framework directory location" ),
         ConfigurationData( "project"           , False , "Project name" ),
         ConfigurationData( "action"            , False , "Action name" ),
         ConfigurationData( "container"         , False , "Indicates is this script must be run in container" ),
      ]
   )



def names( ):
   return config.get_names( )
# def names

def values( name: str ):
   return config.get_values( name )
# def values

def value( name: str, index: int = 0 ):
   return config.get_value( name, index )
# def value



def configure( argv ):
   process_configuration( config, sys.argv[1:] )
# def configure

def info( ):
   config.info( )
# def info
