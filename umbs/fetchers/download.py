import os

import pfw.console
import pfw.shell
import pfw.base.net

import umbs.base
import umbs.fetchers.base



def get_instance( config, **kwargs ):
   return Fetcher( config, **kwargs )

def do_fetch( repo ):
   repo.fetch( )



class Fetcher( umbs.fetchers.base.Fetcher ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__url = self.__config["url"]
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
      pfw.base.net.download( self.__url, self.__target_dir )
   # def sync

   def remove( self ):
      # @TDA: To be implemented
      pass
   # def remove
# class Fetcher
