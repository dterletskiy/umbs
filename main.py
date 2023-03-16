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



if "*" == configuration.value( "project" ):
   for name, project in umbs_projects.items( ):
      project.do_action( configuration.value( "action" ) )
else:
   umbs_projects[ configuration.value( "project" ) ].do_action( configuration.value( "action" ) )








import docker.image
import docker.container
import docker.packages.ubuntu

def docker( ):
   dockerfile = configuration.value( "dockerfile" )

   os_name = configuration.value( "docker_os_name" )
   os_version = configuration.value( "docker_os_version" )
   image_name = configuration.value( "docker_image_name" )
   image_tag = configuration.value( "docker_image_tag" ) # datetime.datetime.now( ).strftime( "%Y.%m.%d_%H.%M.%S" )
   user_id = 1000
   user_gid = 1000
   user_name = configuration.value( "docker_user_name" )
   user_password = configuration.value( "docker_user_password" )
   user_password_salt = configuration.value( "docker_user_password_salt" )
   user_hashed_password = pfw.linux.password.build_hashed_password( user_password, user_password_salt )
   user_workdir = configuration.value( "docker_user_workdir" )
   container_name = configuration.value( "docker_container_name" )
   packages = " ".join( docker.packages.ubuntu.packages_all )
   build_args = [
         f"ARG_OS_NAME={os_name}",
         f"ARG_OS_VERSION={os_version}",
         f"ARG_USER_ID={user_id}",
         f"ARG_USER_GID={user_gid}",
         f"ARG_USER_NAME={user_name}",
         # f"ARG_USER_PASSWORD={user_password}",
         # f"ARG_USER_PASSWORD_SALT={user_password_salt}",
         # f"ARG_USER_HASHED_PASSWORD={user_hashed_password}",
         f"ARG_PACKAGES='{packages}'",
         f"ARG_USER_WORKDIR='{user_workdir}'",
      ]

   volume_mapping = [
         pfw.linux.docker.Container.Mapping( host = f"/mnt/docker/{container_name}", guest = f"/mnt/host" ),
         pfw.linux.docker.Container.Mapping( host = f"~/.ssh", guest = f"/home/{user_name}/.ssh" ),
         pfw.linux.docker.Container.Mapping( host = f"~/.gitconfig", guest = f"/home/{user_name}/.gitconfig" ),
      ]

   port_mapping = [
         pfw.linux.docker.Container.Mapping( host = "5000", guest = "5000" ),
      ]



   docker.image.build(
         dokerfile = dockerfile,
         image_name = image_name,
         image_tag = image_tag,
         build_args = build_args
      )

   docker.container.run(
         container_name = container_name,
         image_name = image_name,
         image_tag = image_tag,
         volume_mapping = volume_mapping,
         port_mapping = port_mapping
      )
# def docker
