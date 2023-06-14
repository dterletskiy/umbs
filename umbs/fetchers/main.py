#!/usr/bin/python

import importlib
import datetime

import pfw.console



class Fetcher:
   def __new__( cls, yaml_data: dict, **kwargs ):
      return object.__new__( cls )
   # def __new__

   def __init__( self, yaml_data: dict, **kwargs ):
      namespase = "umbs.fetchers"
      self.__module = importlib.import_module( f"{namespase}.{yaml_data['type']}", __package__ )
      self.__instance = self.__module.get_instance( yaml_data, **kwargs )
   # def __init__

   def do_fetch( self ):
      begin = datetime.datetime.now( )

      # self.__module.do_fetch( self.__instance )
      self.__instance.do_fetch( )

      end = datetime.datetime.now( )
      pfw.console.debug.info( f"fetcher '{self.__module}': fetch time {end - begin}" )
   # def do_fetch

   def do_remove( self ):
      begin = datetime.datetime.now( )

      # self.__module.do_remove( self.__instance )
      self.__instance.do_remove( )

      end = datetime.datetime.now( )
      pfw.console.debug.info( f"fetcher '{self.__module}': remove time {end - begin}" )
   # def do_remove



   __instance = None
   __module = None
# class Fetcher
