import pfw.console
import pfw.shell

import umbs.base



def get_tool( config, **kwargs ):
   return Tool( config, **kwargs )



class Tool:
   def __init__( self, config, **kwargs ):
      self.__config = config

      if "exe" not in self.__config:
         raise umbs.base.YamlFormatError( f"Filed 'exe' must be defined in tool" )

      self.__exe = self.__config["exe"]
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __setattr__( self, attr, value ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) ]
      if attr in attr_list:
         self.__dict__[ attr ] = value
         return
      raise AttributeError
   # def __setattr__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def info( self, **kwargs ):
      kw_tabs = kwargs.get( "tabs", 0 )
      kw_msg = kwargs.get( "msg", "" )
      pfw.console.debug.info( f"{kw_msg} (type {self.__class__.__name__}):", tabs = ( kw_tabs + 0 ) )
   # def info



   __config: dict = None
   __exe: str = None
# class Tool
