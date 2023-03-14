import pfw.console
import pfw.archive
import pfw.shell
import pfw.linux.git



def get_fetcher( config, destination, **kwargs ):
   return Repo( config, destination, **kwargs )

def do_fetch( repo ):
   repo.fetch( )



class Repo:
   def __init__( self, config, destination, **kwargs ):
      self.__repo = pfw.linux.git.Repo(
            url = config["url"],
            branch = config.get( "branch", None ),
            directory = destination,
            depth = 1
         )
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
      self.__repo.info( )
   # def info

   def fetch( self, **kwargs ):
      self.__repo.clone( )
   # def sync

   def remove( self ):
      self.__repo.remove( )
   # def remove



   __repo: pfw.linux.git.Repo = None
# class Repo
