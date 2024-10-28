import os

import pfw.console
import pfw.shell
import pfw.base.function

import umbs.actors.base



class Actor( umbs.actors.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__(
            config = config,
            exec = [
                  pfw.base.function.Holder( self.prepare ),
                  pfw.base.function.Holder( self.fetch ),
                  pfw.base.function.Holder( self.test )
               ],
            clean = [
                  pfw.base.function.Holder( self.remove )
               ],
            **kwargs
         )

      self.__target_dir = os.path.join( self.__component_dir, "source", self.__config.get( "subdir", "" ) )

      self.__artifacts = [
            os.path.join( self.__target_dir, a ) for a in self.__get_config( "artifacts", [ ] ) if a
         ]
   # def __init__

   def prepare( self, **kwargs ):
      result = pfw.shell.execute( f"mkdir -p {self.__target_dir}" )
      if 0 != result["code"]:
         return False

      return True
   # def prepare

   def fetch( self, **kwargs ):
      pass
   # def fetch

   def remove( self, **kwargs ):
      pass
   # def remove

   def artifacts( self ):
      return self.__artifacts
   # def artifacts
# class Actor
