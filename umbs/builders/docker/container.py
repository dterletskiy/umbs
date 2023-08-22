import os

import pfw.console
import pfw.shell
import pfw.os.environment
import pfw.linux.docker.container

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( umbs.builders.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      for key in ["name", "image"]:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in builder" )

      self.__container_name = self.__config["name"]
      self.__image_name = self.__config["image"]["name"]
      self.__image_tag = self.__config["image"]["tag"]

      self.__volume_mapping = [ ]
      self.__port_mapping = [ ]
      if "mapping" in self.__config:
         if "volume" in self.__config["mapping"]:
            for item in self.__config["mapping"]["volume"]:
               self.__volume_mapping.append(
                     pfw.linux.docker.container.Mapping( host = f"{item['host']}", guest = f"{item['guest']}" )
                  )
         if "port" in self.__config["mapping"]:
            for item in self.__config["mapping"]["port"]:
               self.__port_mapping.append(
                     pfw.linux.docker.container.Mapping( host = f"{item['host']}", guest = f"{item['guest']}" )
                  )

      self.__environment = [ ]
      if "environment" in self.__config:
         for environment in self.__config["environment"]:
            self.__environment.append( pfw.os.environment.Environment( environment ) )
   # def __init__

   def config( self, **kwargs ):
      return True
   # def config

   def build( self, **kwargs ):
      return pfw.linux.docker.container.create(
            container_name = self.__container_name,
            image_name = self.__image_name,
            image_tag = self.__image_tag,
            volume_mapping = self.__volume_mapping,
            port_mapping = self.__port_mapping,
            env = self.__environment
         )
   # def build

   def clean( self, **kwargs ):
      pass
   # def clean
# class Actor
