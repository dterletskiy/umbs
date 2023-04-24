import os

import pfw.console
import pfw.shell
import pfw.linux.git

import umbs.base
import umbs.fetchers.base



def get_instance( config, **kwargs ):
   return Fetcher( config, **kwargs )

def do_fetch( repo ):
   repo.fetch( )



class Fetcher( umbs.fetchers.base.Fetcher ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__repo = pfw.linux.git.Repo(
            url = self.__config["url"],
            branch = self.__config.get( "branch", None ),
            directory = os.path.join( kwargs.get( "project_dir", None ), self.__config.get( "dir", "" ) ),
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
      self.__repo.clone( )
   # def sync

   def remove( self ):
      self.__repo.remove( )
   # def remove
# class Fetcher
