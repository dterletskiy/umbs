import os
import sys

import pfw.console
import pfw.shell
import pfw.linux.docker.container

import umbs.base
import umbs.configuration
import umbs.projects.main






def init_projects( yaml_config ):
   projects_map: dict = { }
   for name in yaml_config.get_projects( ):
      if project := umbs.projects.main.Project( name, yaml_config.get_project( name ), yaml_config.get_variable( "DIRECTORIES.ROOT" ) ):
         projects_map[ name ] = project

   return projects_map
# def init_projects



def run( project, action, umbs_projects ):
   if "*" == project:
      for name, project in umbs_projects.items( ):
         project.do_action( action )
   else:
      umbs_projects[ project ].do_action( action )
# def run



def run_in_container( ):
   cfg_file = "./.gen/umbs_gen.cfg"
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

   container_project = umbs.configuration.value( 'project' )
   container_action = umbs.configuration.value( 'action' )

   command = f""
   command += f" python3 umbs.py"
   command += f" --config={cfg_file}"
   command += f" --project={container_project}"
   command += f" --action={container_action}"
   # command = ""

   pfw.linux.docker.container.exec( container_name, command = command, workdir = container_umbs_dir )
# def run_in_container



def main( ):
   yaml_config: umbs.base.Config = umbs.base.Config( umbs.configuration.value( "yaml_config" ) )
   # yaml_config.info( ) # @TDA: debug
   umbs_projects: dict = init_projects( yaml_config )

   pfw.console.debug.ok( "------------------------- BEGIN -------------------------" )

   project = umbs.configuration.value( "project" )
   action = umbs.configuration.value( "action" )

   if umbs.configuration.value( 'container' ):
      run_in_container( )
   else:
      run( project, action, umbs_projects )

   pfw.console.debug.ok( "-------------------------- END --------------------------" )
# def main
