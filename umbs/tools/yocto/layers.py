import os

import pfw.console
import pfw.shell
import pfw.linux.file

import umbs.tools.base



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( umbs.tools.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      self.__layers = [ os.path.join( self.__component_dir, i ) for i in self.__config.get( "layers", [ ] ) if i ]
   # def __init__

   def exec( self, **kwargs ):
      command = "bitbake-layers add-layer "
      command += f" && bitbake-layers add-layer ".join( self.__layers )
      result = self.execute( f"source poky/oe-init-build-env {self.__product_dir} && {command}" )

      return result["code"]
   # def exec

   def clean( self, **kwargs ):
      result = True

      return result
   # def clean
# class Actor
