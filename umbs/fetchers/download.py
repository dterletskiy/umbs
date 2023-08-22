import os

import pfw.console
import pfw.shell
import pfw.base.net

import umbs.base
import umbs.fetchers.base



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( umbs.fetchers.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__url = self.__config["url"]
   # def __init__

   def fetch( self, **kwargs ):
      return pfw.base.net.download( self.__url, self.__target_dir )
   # def sync

   def remove( self ):
      # @TDA: To be implemented
      return True
   # def remove
# class Actor
