import pfw.console
import pfw.archive
import pfw.shell
import pfw.linux.repo



def get_fetcher( config, destination, **kwargs ):
   return Fetcher( config, destination, **kwargs )

def do_fetch( repo ):
   repo.fetch( )



class Fetcher:
   def __init__( self, config, destination, **kwargs ):
      self.__repo = pfw.linux.repo.Repo(
            destination = destination,
            manifest_url = config.get( "manifest-url", None ),
            manifest_name = config.get( "manifest-name", None ),
            manifest_branch = config.get( "manifest-branch", None ),
            manifest_depth = config.get( "manifest-depth", None ),
            depth = config.get( "depth", 1 )
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
      self.__repo.install( )
      self.__repo.init( )
      self.__repo.sync( )
   # def sync

   def remove( self ):
      pass
   # def remove



   __repo: pfw.linux.repo.Repo = None
# class Fetcher
