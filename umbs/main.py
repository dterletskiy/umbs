import os
import sys

import pfw.console
import pfw.shell
import pfw.linux.docker.container

import umbs.base
import umbs.configuration
import umbs.components.main



def init_components( yaml_config ):
   components_map: dict = { }
   for name in yaml_config.get_components( ):
      if name in components_map:
         raise umbs.base.ConfigurationFormatError( f"component '{name}' redefinition" )
      if component := umbs.components.main.Component( name, yaml_config.get_component( name ), yaml_config.get_variable( "DIRECTORIES.ROOT" ) ):
         components_map[ name ] = component

   return components_map
# def init_components

def print_components( components: dict ):
   for name, component in components.items( ):
      pfw.console.debug.info( f"{name}" )
      # component.info( ) # @TDA: debug
# def print_components



def run( component, action, umbs_components ):
   if umbs.configuration.value( 'test' ):
      pfw.console.debug.warning( "TEST MODE" )
      return

   if "*" == component:
      for name, component in umbs_components.items( ):
         component.do_action( action )
   else:
      umbs_components[ component ].do_action( action )
# def run

def run_in_container( ):
   # container_user_name = "builder"
   # container_base_dir = "/mnt/host"

   # volume_mapping = [
   #       pfw.linux.docker.container.Mapping(
   #             host = umbs.configuration.value( 'umbs' ),
   #             guest = os.path.join( container_base_dir, "umbs" )
   #          ),
   #       pfw.linux.docker.container.Mapping(
   #             host = umbs.configuration.value( 'pfw' ),
   #             guest = os.path.join( container_base_dir, "pfw" )
   #          ),
   #       pfw.linux.docker.container.Mapping(
   #             host = yaml_config.get_variable( "DIRECTORIES.ROOT" ),
   #             guest = os.path.join( container_base_dir, "project" )
   #          ),
   #       pfw.linux.docker2.Container.Mapping(
   #             host = f"~/.ssh",
   #             guest = f"/home/{container_user_name}/.ssh"
   #          ),
   #       pfw.linux.docker2.Container.Mapping(
   #             host = f"~/.gitconfig",
   #             guest = f"/home/{container_user_name}/.gitconfig"
   #          ),
   #    ]

   # port_mapping = [
   #       pfw.linux.docker2.Container.Mapping( host = "5000", guest = "5000" ),
   #    ]



   cfg_file = "./.gen/umbs.cfg"
   cfg_h = open( os.path.join( cfg_file ), "w" )
   for name in umbs.configuration.names( ):
      if name in [ "container", "config", "umbs" ]:
         continue

      for value in umbs.configuration.values( name ):
         if "YAML.DIRECTORIES.ROOT" == name:
            value = umbs.configuration.value( 'container_root_dir' )

         cfg_h.write( f"{name}:         {value}\n" )
   cfg_h.close( )



   container_root_dir = umbs.configuration.value( 'container_root_dir' )
   container_umbs_dir = os.path.join( container_root_dir, "tda/umbs" )
   container_name = umbs.configuration.value( 'container_name' )

   container_component = umbs.configuration.value( 'component' )
   container_action = umbs.configuration.value( 'action' )

   if not pfw.linux.docker.container.is_exists( container_name ):
      return

   if not pfw.linux.docker.container.is_started( container_name ):
      pfw.linux.docker.container.start( container_name )

   command = f" python3 umbs.py"
   command += f" --config={cfg_file}"
   command += f" --component={container_component}"
   command += f" --action={container_action}"

   pfw.linux.docker.container.exec( container_name, command = command, workdir = container_umbs_dir )
# def run_in_container


def main( ):
   yaml_config: umbs.base.Config = umbs.base.Config( umbs.configuration.value( "yaml_config" ) )
   # yaml_config.info( ) # @TDA: debug
   umbs_components: dict = init_components( yaml_config )
   print_components( umbs_components ) # @TDA: debug

   pfw.console.debug.ok( "------------------------- BEGIN -------------------------" )

   component = umbs.configuration.value( "component" )
   action = umbs.configuration.value( "action" )

   if umbs.configuration.value( 'container' ):
      run_in_container( )
   else:
      run( component, action, umbs_components )

   pfw.console.debug.ok( "-------------------------- END --------------------------" )
# def main
