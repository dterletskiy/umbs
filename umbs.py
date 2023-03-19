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



import sys

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
   sys.exit( 255 )



configuration.configure( sys.argv[1:] )
configuration.info( )

##########################################################################
#                                                                        #
#                           End configuration                            #
#                                                                        #
##########################################################################



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

import pfw.console
import pfw.shell
import pfw.base.str
import pfw.base.dict
import pfw.linux.password

import projects.main
import docker.main



class Config:
   def __init__( self, file: str ):
      yaml_fd = open( file, "r" )
      yaml_data = yaml.load( yaml_fd, Loader = yaml.SafeLoader )
      yaml_stream = yaml.compose( yaml_fd )
      yaml_fd.close( )

      self.__variables = yaml_data.get( "variables", { } )
      self.__projects = yaml_data.get( "projects", { } )

      self.__process_yaml_data( self.__variables )
      # pfw.console.debug.info( pfw.base.str.to_string( self.__variables ) )

      self.__process_yaml_data( self.__projects )
      # pfw.console.debug.info( pfw.base.str.to_string( self.__projects ) )
   # def __init__

   def __del__( self ):
      pass
   # def __del__



   def get_variable( self, variable ):
      return pfw.base.dict.get_value( self.__variables, variable )
   # def get_variable

   def set_variable( self, variable, value ):
      pfw.base.dict.set_value( self.__variables, variable, value )
   # def set_variable

   def get_project( self, name: str ):
      return self.__projects[ name ]
   # def get_project

   def get_variables( self ):
      return self.__variables
   # def get_variables

   def get_projects( self ):
      return self.__projects
   # def get_projects



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
      if not isinstance( value, str ):
         pfw.console.debug.warning( f"ERROR: '{value}' is not a string" )
         return ( False, value )

      replaced: bool = False
      if findall := re.findall( r'\$\{(.+?)\}', value ):
         for item in findall:
            value = value.replace( "${" + item + "}", self.get_variable( item ) )
         value = self.__replace( value )[1]
         replaced = True

      return ( replaced, value )
   # def __replace

   def __walk( self, iterable, address: list, value_processor = None ):
      # pfw.console.debug.info( f"-> address = {address}" )

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
      # elif isinstance( iterable, str ):
      else:
         ( replaced, new_value ) = value_processor( iterable )
         if replaced:
            # print( f"address = {address}" )
            # print( f"old_value = {iterable}" )
            # print( f"new_value = {new_value}" )
            for_adaptation.append( Config.AV( address, new_value ) )

      # pfw.console.debug.info( f"<- address = {address}" )

      return for_adaptation
   # def __walk

   def __process_yaml_data( self, yaml_data ):
      for item in self.__walk( yaml_data, [ ], self.__replace ):
         pfw.base.dict.set_value_by_list_of_keys( yaml_data, item.address, item.value )
   # def __process_yaml_data



   __variables: dict = [ ] 
   __projects: dict = [ ]
# class Config




yaml_config: Config = Config( "configuration.yaml" )


umbs_projects: dict = projects.main.Project.builder( yaml_config )



def main( ):
   if "*" == configuration.value( "project" ):
      for name, project in umbs_projects.items( ):
         project.do_action( configuration.value( "action" ) )
   else:
      umbs_projects[ configuration.value( "project" ) ].do_action( configuration.value( "action" ) )
# def main




if __name__ == "__main__":
   pfw.console.debug.ok( "------------------------- BEGIN -------------------------" )
   main( )
   # docker.main.do_build( )
   pfw.console.debug.ok( "-------------------------- END --------------------------" )
