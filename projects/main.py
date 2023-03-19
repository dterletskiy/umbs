#!/usr/bin/python

import os

import pfw.console

import builders.main
import fetchers.main



class Project:
   def __init__( self, name: str, yaml_config ):
      self.__name = name
      self.__dir = os.path.join( yaml_config.get_variable( "DIRECTORIES.ROOT" ), yaml_config.get_project( name )["dir"] )
      self.__fetchers = fetchers.main.Fetcher.creator( self.__dir, yaml_config.get_project( name )["sources"] )
      self.__builders = builders.main.Builder.creator( self.__dir, yaml_config.get_project( name )["builder"] )

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
   def builder( yaml_config ):
      projects: dict = { }
      for name in yaml_config.get_projects( ):
         projects[ name ] = Project( name, yaml_config )

      return projects
   # def builder

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
