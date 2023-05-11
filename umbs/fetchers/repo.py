import os

import pfw.console
import pfw.shell
import pfw.linux.repo

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

      self.__repo = pfw.linux.repo.Repo(
            destination = kwargs.get( "project_dir", None ),
            manifest_url = self.__config.get( "manifest-url", None ),
            manifest_name = self.__config.get( "manifest-name", None ),
            manifest_branch = self.__config.get( "manifest-branch", None ),
            manifest_depth = self.__config.get( "manifest-depth", None ),
            depth = self.__config.get( "depth", 1 )
         )
   # def __init__

   def fetch( self, **kwargs ):
      result = self.__repo.install( )
      if 0 != result["code"]:
         return False

      result = self.__repo.init( )
      if 0 != result["code"]:
         return False

      result = self.__repo.sync( )
      if 0 != result["code"]:
         return False

      return True
   # def sync

   def remove( self ):
      return True
   # def remove
# class Fetcher
