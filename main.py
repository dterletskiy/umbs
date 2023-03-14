#!/usr/bin/python

# Examples:
# 
# CONFIG=./configuration.cfg
# PFW=/mnt/dev/repos/github.com/dterletskiy/python_fw
# ARCH=x86_64
# OS=linux
# ACTION=clean_build
# TARGET=runtime
# 
# 
# 
# ./build.py --config=./${CONFIG} --include=${PFW} --arch=${ARCH} --os=${OS} --action=${ACTION}
# ./build.py --config=./${CONFIG} --arch=${ARCH} --os=${OS} --action=${ACTION}
# 
# In case if variable "INCLUDE" defined with path to "pfw" "--include" option could be omitted.
# If "INCLUDE" variable defined several times in configuration file all mentioned values will be used.



import os
import sys
import subprocess
import re
import yaml
import pprint
import functools
import operator
import copy
import importlib

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



import pfw.console
import pfw.shell
import pfw.base.str
import pfw.base.dict



yaml_fd = open( "configuration.yaml", "r" )
yaml_data = yaml.load( yaml_fd, Loader = yaml.SafeLoader )
yaml_stream = yaml.compose( yaml_fd )



keywords: dict = {
   "variables": None,
   "projects": None
}



yaml_variables = yaml_data.get( "variables", { } )
yaml_projects = yaml_data.get( "projects", { } )



def get_yaml_variable( variable ):
   return pfw.base.dict.get_value( yaml_variables, variable )
# def get_yaml_variable

def set_yaml_variable( variable, value ):
   pfw.base.dict.set_value( yaml_variables, variable, value )
# def set_yaml_variable



import copy

class AV:
   def __init__( self, a, v ):
      self.address = copy.deepcopy( a )
      self.value = copy.deepcopy( v )

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
pfw.console.debug.info( pfw.base.str.to_string( yaml_variables ) )

process_yaml_data( yaml_projects )
pfw.console.debug.info( pfw.base.str.to_string( yaml_projects ) )



fetchers: list = [ ]
builders: list = [ ]

for name, project in yaml_projects.items( ):
   pfw.console.debug.info( f"processing project: '{name}'" )

   for item in project["sources"]:
      pfw.console.debug.info( f"processing fetcher: '{item}'" )
      module = importlib.import_module( f"fetchers.{item['type']}", __package__ )
      fetcher = module.get_fetcher( item, project["dir"] )
      fetchers.append( fetcher )
      module.do_fetch( fetcher )

   for item in project["builder"]:
      pfw.console.debug.info( f"processing builder: '{item}'" )
      module = importlib.import_module( f"builders.{item['type']}", __package__ )
      builder = module.get_builder( item, project["dir"] )
      builders.append( builder )
      module.do_build( builder )
