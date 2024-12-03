import importlib
import os

import pfw.console
import pfw.shell
import pfw.linux.git

import umbs.actors.types
module_fetcher_base = importlib.import_module( f"{umbs.actors.types.eType.FETCHER}.base", __package__ )



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( module_fetcher_base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__repo = pfw.linux.git.Repo(
            url = self.__config["url"],
            branch = self.__config.get( "branch", None ),
            directory = self.__target_dir,
            depth = self.__config.get( "depth", 1 ),
            single_branch = self.__config.get( "single_branch", True ),
            recursive = self.__config.get( "recursive", False ),
         )
   # def __init__

   def fetch( self, **kwargs ):
      return self.__repo.clone( )
   # def sync

   def remove( self ):
      return self.__repo.remove( )
   # def remove
# class Actor
