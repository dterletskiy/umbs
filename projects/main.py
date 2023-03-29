#!/usr/bin/python

import os

import pfw.console
import pfw.shell

import base
import builders.main
import fetchers.main



class Project:
   def __new__( cls, name: str, yaml_config: base.Config ):
      yaml_project = yaml_config.get_project( name )

      if "active" in yaml_project:
         if False == yaml_project["active"]:
            return None

      return object.__new__( cls )
   # def __new__

   def __init__( self, name: str, yaml_config: base.Config ):
      root_dir = yaml_config.get_variable( "DIRECTORIES.ROOT" )
      yaml_project = yaml_config.get_project( name )
      self.__name = name

      if "dir" in yaml_project:
         self.__dir = os.path.join( root_dir, yaml_project["dir"] )
         pfw.shell.execute( f"mkdir -p {self.__dir}" )
      else:
         raise base.YamlFormatError( f"Filed 'dir' must be defined in the project '{name}'" )

      if "sources" in yaml_project:
         self.__fetchers = fetchers.main.Fetcher.creator( yaml_project["sources"], self.__dir, root_dir = root_dir )
      else:
         self.__fetchers = [ ]
         pfw.console.debug.warning( f"Filed 'sources' is not defined in the project '{name}'" )

      if "builder" in yaml_project:
         self.__builders = builders.main.Builder.creator( yaml_project["builder"], self.__dir, root_dir = root_dir )
      else:
         self.__builders = [ ]
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
