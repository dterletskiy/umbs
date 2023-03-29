#!/usr/bin/python

import importlib



class Builder:
   def __init__( self, yaml_builder: dict, dir: str, **kwargs ):
      self.__dir = dir
      self.__module = importlib.import_module( f"builders.{yaml_builder['type']}", __package__ )
      self.__builder = self.__module.get_builder( yaml_builder, dir, **kwargs )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   @staticmethod
   def creator( yaml_builders: list, dir: str, **kwargs ):
      return [ Builder( yaml_builder, dir, **kwargs ) for yaml_builder in yaml_builders ]
   # def creator

   def do_build( self ):
      self.__module.do_build( self.__builder )
   # def do_build

   __dir: str = None
   __builder = None
   __module = None
# class Builder
