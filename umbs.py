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

import pfw.console
import pfw.shell

import base
import docker.main
import projects.main
import tools.main






def init_projects( yaml_config ):
   projects_map: dict = { }
   for name in yaml_config.get_projects( ):
      if project := projects.main.Project( name, yaml_config.get_project( name ), yaml_config.get_variable( "DIRECTORIES.ROOT" ) ):
         projects_map[ name ] = project

   return projects_map
# def init_projects

def init_tools( yaml_config ):
   tools_map: dict = { }
   for name in yaml_config.get_tools( ):
      if tool := tools.main.Tool( name, yaml_config.get_tool( name ), yaml_config.get_variable( "DIRECTORIES.ROOT" ) ):
         tools_map[ name ] = tool

   return tools_map
# def init_tools



yaml_config: base.Config = base.Config( configuration.value( "yaml_config" ) )
yaml_config.info( )


umbs_projects: dict = init_projects( yaml_config )
umbs_tools: dict = init_tools( yaml_config )



def main( ):
   project = configuration.value( "project" )
   action = configuration.value( "action" )

   if "docker" == project:
      docker.main.do_action( action )
   elif "*" == project:
      for name, project in umbs_projects.items( ):
         project.do_action( action )
   else:
      umbs_projects[ project ].do_action( action )
# def main



if __name__ == "__main__":
   pfw.console.debug.ok( "------------------------- BEGIN -------------------------" )
   main( )
   pfw.console.debug.ok( "-------------------------- END --------------------------" )












class Base:
   def __init__( self, **kwargs ):
      kw_id = kwargs.get( "id", 0 )

      self.__id_base = kw_id
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   # def __setattr__( self, attr, value ):
   #    attr_list = [ i for i in self.__class__.__dict__.keys( ) ]
   #    if attr in attr_list:
   #       self.__dict__[ attr ] = value
   #       return
   #    raise AttributeError
   # # def __setattr__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__



   __id_base: int = 0
# class Base



class Derived( Base ):
   def __init__( self, **kwargs ):
      kw_id = kwargs.get( "id", 0 )

      super( ).__init__( **kwargs )

      self.__id_derived = kw_id
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   # def __setattr__( self, attr, value ):
   #    attr_list = [ i for i in self.__class__.__dict__.keys( ) ]
   #    if attr in attr_list:
   #       self.__dict__[ attr ] = value
   #       return
   #    raise AttributeError
   # # def __setattr__

   def __str__( self ):
      base_attr_list = [ i for i in super( ).__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      pfw.console.debug.info( f"base_attr_list: {base_attr_list}" )
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      pfw.console.debug.info( f"attr_list: {attr_list}" )
      attr_list.extend( base_attr_list )
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__



   __id_derived: int = 0
# class Derived



# item: Derived = Derived( id = 12345 )
# item.__test_filed = 1
# pfw.console.debug.info( item )



class Test:
   def __new__( cls, id ):
      pfw.console.debug.info( )
      return object.__new__( cls )
   # def __new__

   def __init__( self, id, **kwargs ):
      pfw.console.debug.info( )
   # def __init__

   def __del__( self ):
      pfw.console.debug.info( )
   # def __del__

   def __setattr__( self, attr, value ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) ]
      if attr in attr_list:
         self.__dict__[ attr ] = value
         return
      raise AttributeError
   # def __setattr__

   def __str__( self ):
      base_attr_list = [ i for i in super( ).__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      pfw.console.debug.info( f"base_attr_list: {base_attr_list}" )
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      pfw.console.debug.info( f"attr_list: {attr_list}" )
      attr_list.extend( base_attr_list )
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__
# class Test

test = Test( 1 )