import os

import pfw.console
import pfw.shell
import pfw.linux.docker

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Builder( config, **kwargs )

def do_build( builder ):
   builder.config( )
   builder.build( )
   builder.test( )

def do_clean( builder ):
   builder.clean( )



class Builder( umbs.builders.base.Builder ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in ["dockerfile", "image"]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in builder" )

      self.__dockerfile = os.path.join( self.__root_dir, self.__config["dockerfile"] )
      self.__image_name = self.__config["image"]["name"]
      self.__image_tag = self.__config["image"]["tag"]

      self.__build_args = [ ]
      if "from" in self.__config:
         if "name" in self.__config["from"]:
            self.__build_args.append( f"ARG_OS_NAME={self.__config['from']['name']}" )
         if "tag" in self.__config["from"]:
            self.__build_args.append( f"ARG_OS_VERSION={self.__config['from']['tag']}" )
      if "user" in self.__config:
         if "uid" in self.__config["user"]:
            self.__build_args.append( f"ARG_USER_UID={self.__config['user']['uid']}" )
         if "gid" in self.__config["user"]:
            self.__build_args.append( f"ARG_USER_GID={self.__config['user']['gid']}" )
         if "name" in self.__config["user"]:
            self.__build_args.append( f"ARG_USER_NAME={self.__config['user']['name']}" )
         if "password" in self.__config["user"]:
            self.__build_args.append( f"ARG_USER_PASSWORD={self.__config['user']['password']}" )
         if "password_salt" in self.__config["user"]:
            self.__build_args.append( f"ARG_USER_PASSWORD_SALT={self.__config['user']['password_salt']}" )
         if "hashed_password" in self.__config["user"]:
            self.__build_args.append( f"ARG_USER_HASHED_PASSWORD={self.__config['user']['hashed_password']}" )
         if "workdir" in self.__config["user"]:
            self.__build_args.append( f"ARG_USER_WORKDIR={self.__config['user']['workdir']}" )
      if "packages" in self.__config:
         def process_packages( data ):
            pkg = ""

            if isinstance( data, str ):
               pkg = data
            elif isinstance( data, list ) or isinstance( data, tuple ):
               for item in data:
                  pkg += " " + process_packages( item )
            elif isinstance( data, dict ):
               for key, value in data.items( ):
                  pkg += " " + process_packages( value )
            else:
               pfw.console.debug.error( f"unsupported data type: {type(data)}" )

            return pkg
         # def process_packages

         packages = process_packages( self.__config["packages"] )
         self.__build_args.append( f"ARG_PACKAGES='{packages}'" )
   # def __init__

   def __del__( self ):
      pass
   # def __del__

   def __str__( self ):
      attr_list = [ i for i in self.__class__.__dict__.keys( ) if i[:2] != pfw.base.struct.ignore_field ]
      vector = [ f"{str( attr )} = {str( self.__dict__.get( attr ) )}" for attr in attr_list ]
      return self.__class__.__name__ + " { " + ", ".join( vector ) + " }"
   # def __str__

   def config( self, **kwargs ):
      pass
   # def config

   def build( self, **kwargs ):
      pfw.linux.docker.build(
            dokerfile = self.__dockerfile,
            image_name = self.__image_name,
            image_tag = self.__image_tag,
            build_args = self.__build_args
         )
   # def build

   def clean( self, **kwargs ):
      pfw.linux.docker.rmi(
            image_name = self.__image_name,
            image_tag = self.__image_tag
         )
   # def clean
# class Builder
