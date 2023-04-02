#!/usr/bin/python

import importlib



class Tool:
   def __new__( cls, name: str, yaml_tool: dict, root_dir: str ):
      return object.__new__( cls )
   # def __new__

   def __init__( self, name: str, yaml_tool: dict, root_dir: str ):
      self.__module = importlib.import_module( f"umbs.tools.{yaml_tool['type']}", __package__ )
      self.__tool = self.__module.get_tool( yaml_tool )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   __tool = None
   __module = None
# class Tool
