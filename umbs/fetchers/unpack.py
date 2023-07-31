import os

import pfw.console
import pfw.shell
import pfw.linux.file

import umbs.base
import umbs.fetchers.base
import umbs.tools.unpack



def get_instance( config, **kwargs ):
   return Fetcher( config, **kwargs )
# def get_instance



class Fetcher( umbs.fetchers.base.Fetcher ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__unpacker = umbs.tools.unpack.Tool( config, **kwargs )
   # def __init__

   def fetch( self, **kwargs ):
      return self.__unpacker.exec( )
   # def fetch

   def remove( self, **kwargs ):
      return self.__unpacker.clean( )
   # def remove
# class Fetcher
