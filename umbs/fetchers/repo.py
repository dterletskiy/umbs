import os

import pfw.console
import pfw.shell
import pfw.linux.repo

import umbs.base
import umbs.fetchers.base



def get_instance( config, **kwargs ):
   return Fetcher( config, **kwargs )

def do_fetch( repo ):
   repo.fetch( )



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

   def __del__( self ):
      pass
   # def __del__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def fetch( self, **kwargs ):
      self.__repo.install( )
      self.__repo.init( )
      self.__repo.sync( )
   # def sync

   def remove( self ):
      pass
   # def remove
# class Fetcher
