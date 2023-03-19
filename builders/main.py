#!/usr/bin/python

import importlib



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
