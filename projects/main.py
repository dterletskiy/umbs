#!/usr/bin/python

import os

import pfw.console
import pfw.shell

import base
import builders.main
import fetchers.main



class Project:
   def __new__( cls, name: str, yaml_project: dict, root_dir: str ):
      if "active" in yaml_project:
         if False == yaml_project["active"]:
            return None

      return object.__new__( cls )
   # def __new__

   def __init__( self, name: str, yaml_project: dict, root_dir: str ):
      self.__name = name

      if "dir" in yaml_project:
         self.__dir = os.path.join( root_dir, yaml_project["dir"] )
         pfw.shell.execute( f"mkdir -p {self.__dir}" )
      else:
         raise base.YamlFormatError( f"Filed 'dir' must be defined in the project '{name}'" )

      self.__fetchers = [ ]
      if "sources" in yaml_project:
         for yaml_source in yaml_project["sources"]:
            self.__fetchers.append( fetchers.main.Fetcher( yaml_source, self.__dir, root_dir = root_dir ) )
      else:
         pfw.console.debug.warning( f"Filed 'sources' is not defined in the project '{name}'" )

      self.__builders = [ ]
      if "builders" in yaml_project:
         for yaml_builder in yaml_project["builders"]:
            self.__builders.append( builders.main.Builder( yaml_builder, self.__dir, root_dir = root_dir ) )
      else:
         pfw.console.debug.warnin( f"Filed 'builder' must be defined in the project '{name}'" )

      self.__action_map = {
         "fetch": [ self.do_fetch ],
         "build": [ self.do_build ],
         "*": [ self.do_fetch, self.do_build ],
      }
   # def __init__

   def __del__( self ):
      pass
   # def __del__

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

   def do_build( self ):
      for builder in self.__builders:
         builder.do_build( )
   # def do_build

   def do_action( self, action: str ):
      processors = self.__action_map.get( action, [ lambda: pfw.console.debug.error( f"undefined action '{action}'" ) ] )
      for processor in processors:
         processor( )
   # def do_action



   __name: str = None
   __dir: str = None
   __fetchers: list = None
   __builders: list = None

   __action_map: dict = None
# class Project
