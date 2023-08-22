#!/usr/bin/python

import enum

import pfw.console



class eStatus( enum.Enum ):
   def __str__( self ):
      return str( self.value )

   CLEAR = "CLEAR"
   PROCESSING = "PROCESSING"
   READY = "READY"
   ERROR = "ERROR"
# class eStatus

class eType( enum.Enum ):
   def __str__( self ):
      return str( self.value )

   FETCHER = "umbs.fetchers"
   BUILDER = "umbs.builders"
   TOOL = "umbs.tools"
# class eType
