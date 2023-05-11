import os

import pfw.console
import pfw.shell
import pfw.base.net

import umbs.base
import umbs.fetchers.base



def get_instance( config, **kwargs ):
   return Fetcher( config, **kwargs )
# def get_instance

def do_fetch( fetcher ):
   if not fetcher.fetch( ):
      pfw.console.debug.error( "fetch error" )
      return False

   return True
# def do_fetch

def do_remove( fetcher ):
   if not fetcher.remove( ):
      pfw.console.debug.error( "remove error" )
      return False

   return True
# def do_fetch



class Fetcher( umbs.fetchers.base.Fetcher ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__url = self.__config["url"]
   # def __init__

   def fetch( self, **kwargs ):
      result = pfw.base.net.download( self.__url, self.__target_dir )
      return 0 == result["code"]
   # def sync

   def remove( self ):
      # @TDA: To be implemented
      return True
   # def remove
# class Fetcher
