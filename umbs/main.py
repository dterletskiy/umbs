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
      if component := umbs.components.main.Component( name, yaml_config.get_component( name ), yaml_config.get_variable( "DIRECTORIES.ROOT" ) ):
         components_map[ name ] = component

   return components_map
# def init_components



def run( component, action, umbs_components ):
   if "*" == component:
      for name, component in umbs_components.items( ):
         component.do_action( action )
   else:
      umbs_components[ component ].do_action( action )
# def run



def run_in_container( ):
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

   command = f""
   command += f" python3 umbs.py"
   command += f" --config={cfg_file}"
   command += f" --component={container_component}"
   command += f" --action={container_action}"
   # command = ""

   pfw.linux.docker.container.exec( container_name, command = command, workdir = container_umbs_dir )
# def run_in_container



def main( ):
   yaml_config: umbs.base.Config = umbs.base.Config( umbs.configuration.value( "yaml_config" ) )
   # yaml_config.info( ) # @TDA: debug
   umbs_components: dict = init_components( yaml_config )

   pfw.console.debug.ok( "------------------------- BEGIN -------------------------" )

   component = umbs.configuration.value( "component" )
   action = umbs.configuration.value( "action" )

   if umbs.configuration.value( 'container' ):
      run_in_container( )
   else:
      run( component, action, umbs_components )

   pfw.console.debug.ok( "-------------------------- END --------------------------" )
# def main
