#!/usr/bin/python

import os

import pfw.console
import pfw.shell

import umbs.base
import umbs.builders.main
import umbs.fetchers.main
import umbs.tools.main



class Project:
   def __new__( cls, name: str, yaml_project: dict, root_dir: str ):
      if "active" in yaml_project:
         if False == yaml_project["active"]:
            return None

      return object.__new__( cls )
   # def __new__

   def __init__( self, name: str, yaml_project: dict, root_dir: str ):
      self.__name = name

      for key in [ "dir" ]:
         if key not in yaml_project:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in the project '{name}'" )


      self.__dir = os.path.join( root_dir, yaml_project["dir"] )
      pfw.shell.execute( f"mkdir -p {self.__dir}" )

      self.__fetchers = [ ]
      if "sources" in yaml_project:
         for yaml_source in yaml_project["sources"]:
            self.__fetchers.append( umbs.fetchers.main.Fetcher( yaml_source, self.__dir, root_dir = root_dir ) )
      else:
         pfw.console.debug.warning( f"Filed 'sources' is not defined in the project '{name}'" )

      self.__builders = [ ]
      if "builders" in yaml_project:
         for yaml_builder in yaml_project["builders"]:
            self.__builders.append( umbs.builders.main.Builder( yaml_builder, self.__dir, root_dir = root_dir ) )
      else:
         pfw.console.debug.warning( f"Filed 'builder' must be defined in the project '{name}'" )

      self.__tools = [ ]
      if "patches" in yaml_project:
         for yaml_tool in yaml_project["patches"]:
            self.__tools.append( umbs.tools.main.Tool( yaml_tool, self.__dir, root_dir = root_dir ) )
      else:
         pfw.console.debug.warning( f"Filed 'patches' must be defined in the project '{name}'" )

      self.__action_map = {
         "fetch": [ self.do_fetch ],
         "patch": [ self.do_patch ],
         "build": [ self.do_build ],
         "clean": [ self.do_clean ],
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
      projects: dict = { }
      for name in yaml_config.get_projects( ):
         if project := Project( name, yaml_config ):
            projects[ name ] = project

      return projects
   # def creator

   def do_fetch( self ):
      for fetcher in self.__fetchers:
         fetcher.do_fetch( )
   # def do_fetch

   def do_patch( self ):
      for tool in self.__tools:
         tool.do_exec( )
   # def do_patch

   def do_build( self ):
      for builder in self.__builders:
         builder.do_build( )
   # def do_build

   def do_clean( self ):
      for builder in self.__builders:
         builder.do_clean( )
   # def do_clean

   def do_action( self, action: str ):
      processors = self.__action_map.get( action, [ lambda: pfw.console.debug.error( f"undefined action '{action}'" ) ] )
      for processor in processors:
         processor( )
   # def do_action



   __name: str = None
   __dir: str = None
   __fetchers: list = None
   __tools: list = None
   __builders: list = None

   __action_map: dict = None
# class Project
