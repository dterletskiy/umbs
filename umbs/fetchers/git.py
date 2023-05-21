import os

import pfw.console
import pfw.shell
import pfw.linux.git

import umbs.base
import umbs.fetchers.base



def get_instance( config, **kwargs ):
   return Fetcher( config, **kwargs )
# def get_instance



class Fetcher( umbs.fetchers.base.Fetcher ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__repo = pfw.linux.git.Repo(
            url = self.__config["url"],
            branch = self.__config.get( "branch", None ),
            directory = self.__target_dir,
            depth = self.__config.get( "depth", 1 )
         )
   # def __init__

   def fetch( self, **kwargs ):
      return self.__repo.clone( )
   # def sync

   def remove( self ):
      return self.__repo.remove( )
   # def remove
# class Fetcher
