import os

import pfw.console
import pfw.shell
import pfw.linux.repo

import umbs.base
import umbs.fetchers.base



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( umbs.fetchers.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )


      for key in [ "manifest" ]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in fetcher" )

      self.__repo = pfw.linux.repo.Repo(
            destination = self.__target_dir,
            manifest_url = self.__config["manifest"].get( "url", None ),
            manifest_name = self.__config["manifest"].get( "name", None ),
            manifest_branch = self.__config["manifest"].get( "branch", None ),
            manifest_depth = self.__config["manifest"].get( "depth", None ),
            depth = self.__config.get( "depth", 1 )
         )
   # def __init__

   def fetch( self, **kwargs ):
      if False == self.__repo.install( ):
         return False

      if False == self.__repo.init( ):
         return False

      if False == self.__repo.sync( ):
         return False

      return True
   # def sync

   def remove( self ):
      return True
   # def remove
# class Actor
