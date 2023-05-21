#!/usr/bin/python

import importlib



class Fetcher:
   def __new__( cls, yaml_data: dict, **kwargs ):
      return object.__new__( cls )
   # def __new__

   def __init__( self, yaml_data: dict, **kwargs ):
      namespase = "umbs.fetchers"
      self.__module = importlib.import_module( f"{namespase}.{yaml_data['type']}", __package__ )
      self.__instance = self.__module.get_instance( yaml_data, **kwargs )
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

   def do_fetch( self ):
      # self.__module.do_fetch( self.__instance )
      self.__instance.do_fetch( )
   # def do_fetch

   def do_remove( self ):
      # self.__module.do_remove( self.__instance )
      self.__instance.do_remove( )
   # def do_remove



   __instance = None
   __module = None
# class Fetcher
