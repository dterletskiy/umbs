#!/usr/bin/python

# Examples:
# 
# CONFIG=./configuration.cfg
# PFW=/mnt/dev/repos/github.com/dterletskiy/python_fw
# RPOJECT="u-boot"
# ACTION=clean_build
# 
# 
# 
# ./main.py --config=./${CONFIG}
# ./main.py --config=./${CONFIG} --include=${PFW}
# ./main.py --config=./${CONFIG} --project=${RPOJECT}
# ./main.py --config=./${CONFIG} --action=${ACTION}
# ./main.py --config=./${CONFIG} --project=${RPOJECT} --action=${ACTION}
# 
# In case if variable "INCLUDE" defined with path to "pfw" "--include" option could be omitted.
# If "INCLUDE" variable defined several times in configuration file all mentioned values will be used.



import os
import sys
import subprocess
import copy
import re
import yaml
import pprint
import functools
import operator
import copy
import importlib
import datetime

import configuration



##########################################################################
#                                                                        #
#                          Begin configuration                           #
#                                                                        #
##########################################################################

MIN_PYTHON = (3, 8)
if sys.version_info < MIN_PYTHON:
   print( "Python minimal required version is %s.%s" % MIN_PYTHON )
   print( "Current version is %s.%s" % ( sys.version_info.major, sys.version_info.minor ) )
   sys.exit( )



configuration.configure( sys.argv[1:] )
configuration.info( )



import pfw.console
import pfw.shell
import pfw.base.str
import pfw.base.dict
import pfw.linux.password

import docker.main



yaml_fd = open( "configuration.yaml", "r" )
yaml_data = yaml.load( yaml_fd, Loader = yaml.SafeLoader )
yaml_stream = yaml.compose( yaml_fd )
yaml_fd.close( )



yaml_variables = yaml_data.get( "variables", { } )
yaml_projects = yaml_data.get( "projects", { } )



def get_yaml_variable( variable ):
   return pfw.base.dict.get_value( yaml_variables, variable )
# def get_yaml_variable

def set_yaml_variable( variable, value ):
   pfw.base.dict.set_value( yaml_variables, variable, value )
# def set_yaml_variable



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

def replace( value ):
   if not isinstance( value, str ):
      pfw.console.debug.warning( f"ERROR: '{value}' is not a string" )
      return ( False, value )

   replaced: bool = False
   if findall := re.findall( r'\$\{(.+?)\}', value ):
      for item in findall:
         value = value.replace( "${" + item + "}", get_yaml_variable( item ) )
      value = replace( value )[1]
      replaced = True

   return ( replaced, value )
# def replace

def walk( iterable, address: list, value_processor = None ):
   # pfw.console.debug.info( f"-> address = {address}" )

   for_adaptation: list = [ ]
   if isinstance( iterable, dict ):
      for key, value in iterable.items( ):
         new_address = address
         new_address.append( key )
         for_adaptation.extend( walk( value, new_address, value_processor ) )
         del address[-1]
   elif isinstance( iterable, list ) or isinstance( iterable, tuple ):
      for index, item in enumerate( iterable ):
         new_address = address
         new_address.append( index )
         for_adaptation.extend( walk( item, new_address, value_processor ) )
         del address[-1]
   # elif isinstance( iterable, str ):
   else:
      ( replaced, new_value ) = value_processor( iterable )
      if replaced:
         # print( f"address = {address}" )
         # print( f"old_value = {iterable}" )
         # print( f"new_value = {new_value}" )
         for_adaptation.append( AV( address, new_value ) )

   # pfw.console.debug.info( f"<- address = {address}" )

   return for_adaptation
# def walk

def process_yaml_data( yaml_data ):
   for item in walk( yaml_data, [ ], replace ):
      pfw.base.dict.set_value_by_list_of_keys( yaml_data, item.address, item.value )
# def process_yaml_data



process_yaml_data( yaml_variables )
# pfw.console.debug.info( pfw.base.str.to_string( yaml_variables ) )

process_yaml_data( yaml_projects )
# pfw.console.debug.info( pfw.base.str.to_string( yaml_projects ) )



class Fetcher:
   def __init__( self, dir: str, yaml_fetcher: dict ):
      self.__dir = dir
      self.__module = importlib.import_module( f"fetchers.{yaml_fetcher['type']}", __package__ )
      self.__fetcher = self.__module.get_fetcher( yaml_fetcher, dir )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   @staticmethod
   def creator( dir: str, yaml_fetchers: list ):
      return [ Fetcher( dir, yaml_fetcher ) for yaml_fetcher in yaml_fetchers ]
   # def creator

   def do_fetch( self ):
      self.__module.do_fetch( self.__fetcher )
   # def do_fetch

   __dir: str = None
   __fetcher = None
   __module = None
# class Fetcher

class Builder:
   def __init__( self, dir: str, yaml_builder: dict ):
      self.__dir = dir
      self.__module = importlib.import_module( f"builders.{yaml_builder['type']}", __package__ )
      self.__builder = self.__module.get_builder( yaml_builder, dir )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   @staticmethod
   def creator( dir: str, yaml_builders: list ):
      return [ Builder( dir, yaml_builder ) for yaml_builder in yaml_builders ]
   # def creator

   def do_build( self ):
      self.__module.do_build( self.__builder )
   # def do_build

   __dir: str = None
   __builder = None
   __module = None
# class Builder

class Project:
   def __init__( self, name: str, yaml_project: dict ):
      self.__name = name
      self.__dir = yaml_project["dir"]
      self.__fetchers = Fetcher.creator( self.__dir, yaml_project["sources"] )
      self.__builders = Builder.creator( self.__dir, yaml_project["builder"] )

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
   def builder( yaml_projects ):
      projects: dict = { }
      for name, yaml_project in yaml_projects.items( ):
         projects[ name ] = Project( name, yaml_project )

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



umbs_projects: dict = Project.builder( yaml_projects )



def main( ):
   if "*" == configuration.value( "project" ):
      for name, project in umbs_projects.items( ):
         project.do_action( configuration.value( "action" ) )
   else:
      umbs_projects[ configuration.value( "project" ) ].do_action( configuration.value( "action" ) )
# def main




if __name__ == "__main__":
   pfw.console.debug.ok( "------------------------- BEGIN -------------------------" )
   # main( )
   docker.main.do_build( )
   pfw.console.debug.ok( "-------------------------- END --------------------------" )
