import os
import sys

import pfw.console
import pfw.shell
import pfw.linux.docker.container

import umbs.base
import umbs.configuration
import umbs.components.main



def run( **kwargs ):
   kw_umbs_components = kwargs.get( "umbs_components", None )

   component = umbs.configuration.value( "component" )
   action = umbs.configuration.value( "action" )
   targets = umbs.configuration.values( "target" )

   if umbs.configuration.value( 'test' ):
      pfw.console.debug.warning( "TEST MODE" )
      return

   if "*" == component:
      for _name, _component in kw_umbs_components.items( ):
         _component.do_action( action, targets = targets )
   else:
      if component in kw_umbs_components:
         kw_umbs_components[ component ].do_action( action, targets = targets )
      else:
         pfw.console.debug.error( f"undefined component '{component}'" )
# def run

def run_in_container( ):
   cfg_file = "./.gen/umbs.cfg"
   cfg_h = open( os.path.join( cfg_file ), "w" )
   for name in umbs.configuration.names( ):
      if name in [ "container", "config", "umbs", "YAML.DIRECTORIES.ROOT" ]:
         continue

      for value in umbs.configuration.values( name ):
         cfg_h.write( f"{name}:         {value}\n" )

   cfg_h.write( f"YAML.DIRECTORIES.ROOT:         {umbs.configuration.value( 'container_root_dir' )}\n" )
   cfg_h.close( )



   container_root_dir = umbs.configuration.value( 'container_root_dir' )
   container_umbs_dir = os.path.join( container_root_dir, "tda/umbs" )
   container_name = umbs.configuration.value( 'container_name' )

   container_component = umbs.configuration.value( 'component' )
   container_action = umbs.configuration.value( 'action' )
   container_target = umbs.configuration.value( 'target' )

   if not pfw.linux.docker.container.is_exists( container_name ):
      return

   if not pfw.linux.docker.container.is_started( container_name ):
      pfw.linux.docker.container.start( container_name )

   command = f" python3 umbs.py --config={cfg_file}"
   command += f" --test" if umbs.configuration.value( 'test' ) else ""
   pfw.linux.docker.container.exec( container_name, command = command, workdir = container_umbs_dir )
# def run_in_container


def main( ):
   yaml_config: umbs.base.Config = umbs.base.Config( umbs.configuration.value( "yaml_config" ), verbose = True )
   umbs_components: dict = umbs.components.main.init( yaml_config, verbose = True )

   pfw.console.debug.ok( "------------------------- BEGIN -------------------------" )

   if umbs.configuration.value( 'container' ):
      run_in_container( )
   else:
      run( umbs_components = umbs_components )

   pfw.console.debug.ok( "-------------------------- END --------------------------" )
# def main
