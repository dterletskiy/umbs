#!/usr/bin/python

import importlib
import datetime

import pfw.console



class Builder:
   def __new__( cls, yaml_data: dict, **kwargs ):
      return object.__new__( cls )
   # def __new__

   def __init__( self, yaml_data: dict, **kwargs ):
      namespase = "umbs.builders"
      self.__module = importlib.import_module( f"{namespase}.{yaml_data['type']}", __package__ )
      self.__instance = self.__module.get_instance( yaml_data, **kwargs )
   # def __init__

   def do_build( self ):
      begin = datetime.datetime.now( )

      # self.__module.do_build( self.__instance )
      self.__instance.do_build( )

      end = datetime.datetime.now( )
      pfw.console.debug.info( f"builder '{self.__module}': build time {end - begin}" )
   # def do_build

   def do_clean( self ):
      begin = datetime.datetime.now( )

      # self.__module.do_clean( self.__instance )
      self.__instance.do_clean( )

      end = datetime.datetime.now( )
      pfw.console.debug.info( f"builder '{self.__module}': clean time {end - begin}" )
   # def do_clean



   __instance = None
   __module = None
# class Builder
