#!/usr/bin/python

import importlib



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
