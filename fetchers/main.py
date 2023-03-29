#!/usr/bin/python

import importlib



class Fetcher:
   def __new__( cls, yaml_fetcher: dict, dir: str, **kwargs ):
      return object.__new__( cls )
   # def __new__

   def __init__( self, yaml_fetcher: dict, dir: str, **kwargs ):
      self.__dir = dir
      self.__module = importlib.import_module( f"fetchers.{yaml_fetcher['type']}", __package__ )
      self.__fetcher = self.__module.get_fetcher( yaml_fetcher, dir, **kwargs )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   @staticmethod
   def creator( yaml_fetchers: list, dir: str, **kwargs ):
      return [ Fetcher( yaml_fetcher, dir, **kwargs ) for yaml_fetcher in yaml_fetchers ]
   # def creator

   def do_fetch( self ):
      self.__module.do_fetch( self.__fetcher )
   # def do_fetch

   __dir: str = None
   __fetcher = None
   __module = None
# class Fetcher
