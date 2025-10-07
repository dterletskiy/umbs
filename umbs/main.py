import os
import sys
import re

import pfw.console
import pfw.shell
import pfw.base.yaml
import pfw.base.function
import pfw.linux.docker.container
import pfw.linux.docker.image

import umbs.configuration
import umbs.variables
import umbs.components.main



def run( umbs_components, **kwargs ):
   component = umbs.configuration.value( "component" )
   action = umbs.configuration.value( "action" )
   targets = umbs.configuration.values( "target" )

   if umbs.configuration.value( 'test' ):
      pfw.console.debug.warning( "TEST MODE" )
      return

   if component in ("*", "world", "all"):
      for _name, _component in umbs_components.items( ):
         _component.do_action( action, targets = targets )
   else:
      if component in umbs_components:
         umbs_components[ component ].do_action( action, targets = targets )
      else:
         pfw.console.debug.error( f"undefined component '{component}'" )
# def run

def run_in_container( docker_image_name, **kwargs ):

   container_root_dir = "/mnt/host"
   host_project_dir = umbs.configuration.value( "YAML.DIRECTORIES.ROOT" )
   container_project_dir = os.path.join( container_root_dir, "project" )
   host_umbs_dir = umbs.configuration.value( "application" )
   container_umbs_dir = os.path.join( container_root_dir, "umbs" )
   host_pfw_dir = umbs.configuration.value( "pfw" )
   container_pfw_dir = os.path.join( container_root_dir, "pfw" )

   stay_in_container = False
   do_not_remove_container = False

   # Generation configuration file from command line and passed configuration file
   # to execute 'umbs' inside the docker container using this configuration file
   cfg_file = "./.gen/umbs.cfg"
   cfg_h = open( cfg_file, "w" )
   for name in umbs.configuration.names( ):
      # Skip parameters what must not be present in config for container execution
      # because they will be substituted or should not be at all
      if name in [ "container_from", "config", "application", "YAML.DIRECTORIES.ROOT" ]:
         continue
      # Replacing 'pfw' path corresponding to container path
      if name == "pfw":
         cfg_h.write( f"{name}:         {container_pfw_dir}\n" )
      # Write all values for each parameter
      for value in umbs.configuration.values( name ):
         cfg_h.write( f"{name}:         {value}\n" )
   cfg_h.write( f"YAML.DIRECTORIES.ROOT:         {container_project_dir}\n" )
   cfg_h.close( )




   if not pfw.linux.docker.image.is_exists( docker_image_name ):
      pfw.console.debug.error( f"image '{docker_image_name}' does not exist" )
      return False

   bash_command = f" python3 umbs.py --config={cfg_file}"
   bash_command += f" --test" if umbs.configuration.value( 'test' ) else ""
   if stay_in_container:
      bash_command += "; exec bash"
   command = f"bash -c \"{bash_command}\""
   # command = "bash"

   mapping_list = [
         pfw.linux.docker.container.Mapping(
               "~/.ssh", "/home/builder/.ssh"
            ),
         pfw.linux.docker.container.Mapping(
               "~/.gitconfig", "/home/builder/.gitconfig"
            ),
         pfw.linux.docker.container.Mapping(
               host_project_dir, container_project_dir
            ),
         pfw.linux.docker.container.Mapping(
               host_umbs_dir, container_umbs_dir
            ),
         pfw.linux.docker.container.Mapping(
               host_pfw_dir, container_pfw_dir
            )
      ]

   pfw.linux.docker.container.run(
         "android_builder",
         docker_image_name,
         command = command,
         workdir = container_umbs_dir,
         volume_mapping = mapping_list,
         disposable = not do_not_remove_container
      )

   return True
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

   umbs.variables.root = yaml_config.get_variable( "DIRECTORIES.ROOT" )
# def yaml_postprocessor



def main( ):
   # Processing configuration yaml file to obtaine yaml database.
   # This is first stage processing.
   yaml_config: pfw.base.yaml.Processor = pfw.base.yaml.Processor(
      file = umbs.configuration.value( "yaml_config" ),
      critical_variables = [ "DIRECTORIES.ROOT" ],
      root_nodes = [ "components" ],
      verbose = False,
      gen_dir = "./.gen/1",
      postprocessor = pfw.base.function.Holder( yaml_postprocessor )
   )

   # Building components list and objects.
   # This is the first stage.
   # On this stage all "internal" variables for each component will be created
   # and corresponding references in yaml file will be replaces with coresponding
   # values on the next stage.
   umbs_components: dict = umbs.components.main.init( yaml_config, verbose = True )

   # Reading grenerated processed yaml configuration file stored during
   # processing yaml configuration file on the first stage.
   yaml_lines = ""
   with open( yaml_config.processed_yaml( ), 'r' ) as file:
      yaml_lines = file.read( )

   # Replacing internal variables to their values generated during building
   # components list on the first stage.
   pattern = r'\%\{([^{}]+)\}'
   detected = True
   while True == detected:
      yaml_lines_processed: str = ""
      detected = False
      for yaml_line in yaml_lines.split( "\n" ):
         if findall := re.findall( pattern, yaml_line ):
            detected = True
            for item in findall:
               value = umbs.variables.get_value( item, None, verbose = True )
               if None == value:
                  pfw.console.debug.error( yaml_line )
                  raise pfw.base.yaml.YamlFormatError( f"no variable name '{item}'" )
               yaml_line = yaml_line.replace( "%{" + item + "}", str(value) )
         yaml_lines_processed += yaml_line + "\n"
      yaml_lines = yaml_lines_processed

   # Processing configuration yaml file to obtaine yaml database.
   # This is second stage processing.
   yaml_config = pfw.base.yaml.Processor(
      string = yaml_lines,
      verbose = False,
      gen_dir = "./.gen/2"
   )

   # Building components list and objects.
   # This is the second stage.
   umbs_components: dict = umbs.components.main.init( yaml_config, verbose = True )



   pfw.console.debug.ok( "------------------------- BEGIN -------------------------" )

   if docker_image_name := umbs.configuration.value( 'container_from' ):
      run_in_container( docker_image_name )
   else:
      run( umbs_components )

   pfw.console.debug.ok( "-------------------------- END --------------------------" )
# def main
