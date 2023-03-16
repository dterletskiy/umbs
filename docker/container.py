#!/usr/bin/python3

import pfw.console
import pfw.shell
import pfw.linux.docker



def run( **kwargs ):
   kw_container_name = kwargs.get( "container_name", None )
   kw_hostname = kwargs.get( "hostname", "host" )
   kw_image_name = kwargs.get( "image_name", None )
   kw_image_tag = kwargs.get( "image_tag", None )
   kw_volume_mapping = kwargs.get( "volume_mapping", { } )
   kw_port_mapping = kwargs.get( "port_mapping", { } )

   container: pfw.linux.docker.Container = pfw.linux.docker.Container(
         name = kw_container_name,
         hostname = kw_hostname,
         image = f"{kw_image_name}:{kw_image_tag}",
         volume_mapping = kw_volume_mapping,
         port_mapping = kw_port_mapping
      )
   container.run( disposable = True )
# def run
