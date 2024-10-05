import os
import sys

import pfw.console
import pfw.shell
import pfw.base.yaml
import pfw.base.function
import pfw.linux.docker.container

import umbs.configuration
import umbs.components.main



def run( umbs_components, **kwargs ):
   component = umbs.configuration.value( "component" )
   action = umbs.configuration.value( "action" )
   targets = umbs.configuration.values( "target" )

   if umbs.configuration.value( 'test' ):
      pfw.console.debug.warning( "TEST MODE" )
      return

   if "*" == component:
      for _name, _component in umbs_components.items( ):
         _component.do_action( action, targets = targets )
   else:
      if component in umbs_components:
         umbs_components[ component ].do_action( action, targets = targets )
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


def yaml_postprocessor( yaml_config: pfw.base.yaml.Processor ):
   pfw.console.debug.warning( "yaml_postprocessor" )
   # Override some variables according to "config" file or command line
   for name in umbs.configuration.names( ):
      if not name.startswith( "YAML." ):
         continue

      replace_name = name.removeprefix( "YAML." )
      replace_value = umbs.configuration.value( name )

      pfw.console.debug.info( f"detected configuration variable '{name}' with value '{replace_value}'" )
      pfw.console.debug.info( f"changing value of variable '{replace_name}'" )
      pfw.console.debug.info( f"'{replace_name}' = '{yaml_config.get_variable( replace_name )}'" )
      yaml_config.set_variable( replace_name, replace_value )
      pfw.console.debug.info( f"'{replace_name}' = '{yaml_config.get_variable( replace_name )}'" )
# def yaml_postprocessor



def main( ):
   yaml_config: pfw.base.yaml.Processor = pfw.base.yaml.Processor(
      umbs.configuration.value( "yaml_config" ),
      critical_variables = [ "DIRECTORIES.ROOT" ],
      root_nodes = [ "components" ],
      verbose = False,
      gen_dir = "./.gen",
      postprocessor = pfw.base.function.Holder( yaml_postprocessor )
   )

   umbs_components: dict = umbs.components.main.init( yaml_config, verbose = True )

   pfw.console.debug.ok( "------------------------- BEGIN -------------------------" )

   if umbs.configuration.value( 'container' ):
      run_in_container( )
   else:
      run( umbs_components )

   pfw.console.debug.ok( "-------------------------- END --------------------------" )
# def main
