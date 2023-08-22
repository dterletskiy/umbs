import os

import pfw.console
import pfw.shell
import pfw.base.function

import umbs.base
import umbs.actors.base



class Actor( umbs.actors.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__(
            config = config,
            exec = [
                  pfw.base.function.Holder( self.prepare ),
                  pfw.base.function.Holder( self.exec ),
                  pfw.base.function.Holder( self.test )
               ],
            clean = [
                  pfw.base.function.Holder( self.clean )
               ],
            **kwargs
         )

      self.__target_dir = os.path.join( self.__component_dir, self.__config.get( "subdir", "" ) )
   # def __init__

   def prepare( self, **kwargs ):
      result = pfw.shell.execute( f"mkdir -p {self.__target_dir}" )
      if 0 != result["code"]:
         return False

      return True
   # def prepare

   def exec( self, **kwargs ):
      return True
   # def exec

   def clean( self, **kwargs ):
      return True
   # def clean

   def test( self, **kwargs ):
      result: bool = True

      for artifact in self.__artifacts:
         if os.path.exists( artifact ):
            pfw.console.debug.ok( f"artifact '{artifact}' exists" )
            pfw.shell.execute( f"file {artifact}", output = pfw.shell.eOutput.PTY )
         else:
            pfw.console.debug.error( f"artifact '{artifact}' does not exist" )
            result = False

      return result
   # def test
# class Actor
