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
