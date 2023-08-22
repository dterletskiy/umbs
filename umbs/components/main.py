#!/usr/bin/python

import os

import pfw.console
import pfw.shell

import umbs.base
import umbs.actors.types
import umbs.actors.main



class Component:
   def __new__( cls, name: str, yaml_component: dict, root_dir: str ):
      if "active" in yaml_component:
         if False == yaml_component["active"]:
            return None

      return object.__new__( cls )
   # def __new__

   def __init__( self, name: str, yaml_component: dict, root_dir: str ):
      self.__name = name

      for key in [ "subdir" ]:
         if key not in yaml_component:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in the component '{name}'" )


      self.__component_dir = os.path.join( root_dir, yaml_component["subdir"] )
      pfw.shell.execute( f"mkdir -p {self.__component_dir}" )

      self.__fetchers = [ ]
      if "sources" in yaml_component:
         for yaml_source in yaml_component["sources"]:
            self.__fetchers.append(
               umbs.actors.main.Actor(
                  type = umbs.actors.types.eType.FETCHER,
                  yaml_data = yaml_source,
                  root_dir = root_dir,
                  component_dir = self.__component_dir
               )
            )
      else:
         # pfw.console.debug.warning( f"Fieled 'sources' is not defined in the component '{name}'" ) # @TDA: debug
         pass

      self.__builders = [ ]
      if "builders" in yaml_component:
         for yaml_builder in yaml_component["builders"]:
            self.__builders.append(
               umbs.actors.main.Actor(
                  type = umbs.actors.types.eType.BUILDER,
                  yaml_data = yaml_builder,
                  root_dir = root_dir,
                  component_dir = self.__component_dir
               )
            )
      else:
         # pfw.console.debug.warning( f"Fieled 'builder' is not defined in the component '{name}'" ) # @TDA: debug
         pass

      self.__tools = [ ]
      if "patches" in yaml_component:
         for yaml_tool in yaml_component["patches"]:
            self.__tools.append(
               umbs.actors.main.Actor(
                  type = umbs.actors.types.eType.TOOL,
                  yaml_data = yaml_tool,
                  root_dir = root_dir,
                  component_dir = self.__component_dir
               )
            )
      else:
         # pfw.console.debug.warning( f"Fieled 'patches' is not defined in the component '{name}'" ) # @TDA: debug
         pass

      self.__action_map = {
         "fetch": [ self.do_fetch ],
         "patch": [ self.do_patch ],
         "build": [ self.do_build ],
         "clean": [ self.do_clean ],
         "clean_build": [ self.do_clean, self.do_build ],
         "*": [ self.do_fetch, self.do_patch, self.do_build ],
      }
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
      attr_list = [ i for i in self.__class__.__dict__.keys( ) ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   @staticmethod
   def creator( yaml_config ):
      components: dict = { }
      for name in yaml_config.get_components( ):
         if component := Component( name, yaml_config ):
            components[ name ] = component

      return components
   # def creator

   def info( self, **kwargs ):
      kw_tabs = kwargs.get( "tabs", kwargs.get( "tabulations", 0 ) )
      kw_message = kwargs.get( "message", "" )
      pfw.console.printf.info( f"{kw_message} (type {self.__class__.__name__}):", tabs = ( kw_tabs + 0 ) )

      pfw.console.printf.info( "name:      \'", self.__name, "\'", tabs = ( kw_tabs + 1 ) )
      pfw.console.printf.info( "directory: \'", self.__component_dir, "\'", tabs = ( kw_tabs + 1 ) )
      pfw.console.printf.info( "fetchers:  \'", len( self.__fetchers ), "\'", tabs = ( kw_tabs + 1 ) )
      for fetcher in self.__fetchers:
         fetcher.info( tabs = kw_tabs + 1 )
      pfw.console.printf.info( "tools:  \'", len( self.__tools ), "\'", tabs = ( kw_tabs + 1 ) )
      for tool in self.__tools:
         tool.info( tabs = kw_tabs + 1 )
      pfw.console.printf.info( "builders:  \'", len( self.__builders ), "\'", tabs = ( kw_tabs + 1 ) )
      for builder in self.__builders:
         builder.info( tabs = kw_tabs + 1 )
   # def info

   def do_fetch( self ):
      for fetcher in self.__fetchers:
         fetcher.do_action( )
   # def do_fetch

   def do_patch( self ):
      for tool in self.__tools:
         tool.do_action( )
   # def do_patch

   def do_build( self ):
      for builder in self.__builders:
         builder.do_action( )
   # def do_build

   def do_clean( self ):
      for builder in self.__builders:
         builder.do_clean( )
   # def do_clean

   def do_action( self, action: str ):
      processors = self.__action_map.get(
            action,
            [ lambda: pfw.console.debug.error( f"undefined action '{action}'" ) ]
         )
      for processor in processors:
         processor( )
   # def do_action



   __name: str = None
   __component_dir: str = None
   __fetchers: list = None
   __tools: list = None
   __builders: list = None

   __action_map: dict = None
# class Component
