#!/usr/bin/python

import importlib
import pfw.console



class Builder:
   def __new__( cls, yaml_builder: dict, dir: str, **kwargs ):
      return object.__new__( cls )
   # def __new__

   def __init__( self, yaml_builder: dict, dir: str, **kwargs ):
      self.__dir = dir
      self.__module = importlib.import_module( f"umbs.builders.{yaml_builder['type']}", __package__ )
      self.__builder = self.__module.get_builder( yaml_builder, dir, **kwargs )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __setattr__( self, attr, value ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) ]
      if attr in attr_list:
         self.__dict__[ attr ] = value
         return
      raise AttributeError
   # def __setattr__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def do_build( self ):
      self.__module.do_build( self.__builder )
   # def do_build

   def do_clean( self ):
      self.__module.do_clean( self.__builder )
   # def do_clean



   __dir: str = None
   __builder = None
   __module = None
# class Builder
