#!/usr/bin/python

import copy
import re
import os
import enum
import yaml

import pfw.console
import pfw.base.str
import pfw.base.dict
import pfw.base.function

import umbs.actors.types



class Actor:
   def __init__( self, **kwargs ):
      self.__status = umbs.actors.types.eStatus.CLEAR

      # self.__type = kwargs["type"]
      self.__config = kwargs["config"]
      self.__root_dir = kwargs["root_dir"]
      self.__component_dir = kwargs["component_dir"]

      self.__dependencies = self.__config.get( "deps", [ ] )
      self.__artifacts = [
            os.path.join( self.__component_dir, a ) for a in self.__config.get( "artifacts", [ ] )
         ]

      self.__export = ""
      for env in self.__config.get( "env", [ ] ):
         self.__export += f" export {env};" if 0 < len( env ) else ""

      self.__functions = {
            "exec": kwargs.get( "exec", [ ] ),
            "clean": kwargs.get( "clean", [ ] ),
         }

      # environment: dict = { }
      # for env in self.__config.get( "env", [ ] ):
      #    env_list = env.split( "=" )
      #    if len( env_list ) not in [1, 2]:
      #       continue
      #    environment[ env_list[0] ] = env_list[1] if 2 == len( env_list ) else ""
      # self.__environment = pfw.os.environment.build( env_add = environment )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def info( self, **kwargs ):
      kw_tabs = kwargs.get( "tabs", 0 )
      kw_msg = kwargs.get( "msg", "" )
      pfw.console.debug.info( f"{kw_msg} (type {self.__class__.__name__}):", tabs = ( kw_tabs + 0 ) )
   # def info

   def do_action( self, **kwargs ):
      self.__status = umbs.actors.types.eStatus.PROCESSING

      for function in self.__functions["exec"]:
         if True != function( **kwargs ):
            pfw.console.debug.error( f"{function.name( )} error" )
            self.__status = umbs.actors.types.eStatus.ERROR
            return self.__status

      self.__status = umbs.actors.types.eStatus.READY
      return self.__status
   # def do_action

   def do_clean( self, **kwargs ):
      self.__status = umbs.actors.types.eStatus.PROCESSING

      for function in self.__functions["clean"]:
         if True != function( **kwargs ):
            pfw.console.debug.error( f"{function.name( )} error" )
            self.__status = umbs.actors.types.eStatus.ERROR
            return self.__status

      self.__status = umbs.actors.types.eStatus.CLEAR
      return self.__status
   # def do_clean



   def component_dir( self ):
      return self.__component_dir
   # def component_dir

   def artifacts( self ):
      return self.__artifacts
   # def artifacts

   def dependencies( self ):
      return self.__dependencies
   # def dependencies



   def execute( self, command, *argv, **kwargs ):
      kwargs["output"] = kwargs.get( "output", pfw.shell.eOutput.PTY )
      kwargs["cwd"] = kwargs.get( "cwd", self.__target_dir )
      if "env" in kwargs: del kwargs["env"] # kwargs["env"] = None # kwargs.get( "env", self.__environment )

      return pfw.shell.execute( f"{self.__export} {command}", *argv, **kwargs )
   # def execute



   def __get_config( self, keys ):
      return pfw.base.dict.get_value( self.__config, keys )
   # def __get_config
# class Actor
