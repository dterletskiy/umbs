#!/usr/bin/python

import importlib
import datetime

import pfw.console

import umbs.actors.types



class Actor:
   def __new__( cls, **kwargs ):
      return object.__new__( cls )
   # def __new__

   def __init__( self, **kwargs ):
      self.__namespase = str( kwargs["type"] )
      self.__yaml_data = kwargs["yaml_data"]
      self.__module = importlib.import_module( f"{self.__namespase}.{self.__yaml_data['type']}", __package__ )
      self.__instance = self.__module.get_instance( self.__yaml_data, **kwargs )
   # def __init__

   def info( self, **kwargs ):
      kw_tabs = kwargs.get( "tabs", kwargs.get( "tabulations", 0 ) )
      kw_message = kwargs.get( "message", "" )
      pfw.console.printf.info( f"{kw_message} (type {self.__class__.__name__}):", tabs = ( kw_tabs + 0 ) )

      pfw.console.printf.info( "module:     \'", self.__module, "\'", tabs = ( kw_tabs + 1 ) )
      self.__instance.info( tabs = kw_tabs + 1 )
   # def info

   def do_action( self, **kwargs ):
      begin = datetime.datetime.now( )
      self.__instance.do_action( **kwargs )
      end = datetime.datetime.now( )
      pfw.console.debug.info( f"'{self.__namespase}' '{self.__module}': action time {end - begin}" )
   # def do_action

   def do_clean( self, **kwargs ):
      begin = datetime.datetime.now( )
      self.__instance.do_clean( **kwargs )
      end = datetime.datetime.now( )
      pfw.console.debug.info( f"'{self.__namespase}' '{self.__module}': clean time {end - begin}" )
   # def do_clean



   __instance = None
   __module = None
# class Actor
