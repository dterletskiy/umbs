#!/usr/bin/python3

import pfw.console
import pfw.shell
import pfw.linux.docker2



def create( **kwargs ):
   kw_container_name = kwargs.get( "container_name", None )
   kw_hostname = kwargs.get( "hostname", "host" )
   kw_image_name = kwargs.get( "image_name", None )
   kw_image_tag = kwargs.get( "image_tag", None )
   kw_volume_mapping = kwargs.get( "volume_mapping", { } )
   kw_port_mapping = kwargs.get( "port_mapping", { } )
   kw_disposable = kwargs.get( "disposable", True )

   container: pfw.linux.docker2.Container = pfw.linux.docker2.Container(
         name = kw_container_name,
         hostname = kw_hostname,
         image = f"{kw_image_name}:{kw_image_tag}",
         volume_mapping = kw_volume_mapping,
         port_mapping = kw_port_mapping
      )
   container.create( disposable = kw_disposable )
# def create

def remove( **kwargs ):
   kw_container_name = kwargs.get( "container_name", None )

   container: pfw.linux.docker2.Container = pfw.linux.docker2.Container(
         name = kw_container_name,
      )
   container.remove( )
# def remove

def start( **kwargs ):
   kw_container_name = kwargs.get( "container_name", None )

   container: pfw.linux.docker2.Container = pfw.linux.docker2.Container(
         name = kw_container_name,
      )
   container.start( )
# def start

def stop( **kwargs ):
   kw_container_name = kwargs.get( "container_name", None )

   container: pfw.linux.docker2.Container = pfw.linux.docker2.Container(
         name = kw_container_name,
      )
   container.stop( )
# def stop

def run( **kwargs ):
   kw_container_name = kwargs.get( "container_name", None )
   kw_hostname = kwargs.get( "hostname", "host" )
   kw_image_name = kwargs.get( "image_name", None )
   kw_image_tag = kwargs.get( "image_tag", None )
   kw_volume_mapping = kwargs.get( "volume_mapping", { } )
   kw_port_mapping = kwargs.get( "port_mapping", { } )
   kw_disposable = kwargs.get( "disposable", True )

   container: pfw.linux.docker2.Container = pfw.linux.docker2.Container(
         name = kw_container_name,
         hostname = kw_hostname,
         image = f"{kw_image_name}:{kw_image_tag}",
         volume_mapping = kw_volume_mapping,
         port_mapping = kw_port_mapping
      )
   container.run( disposable = kw_disposable )
# def run

def exec( **kwargs ):
   kw_container_name = kwargs.get( "container_name", None )

   container: pfw.linux.docker2.Container = pfw.linux.docker2.Container(
         name = kw_container_name,
      )
   container.exec( "bash" )
# def exec
