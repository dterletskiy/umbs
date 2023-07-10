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
   cfg = open( os.path.join( cfg_file ), "w" )
   for name in umbs.configuration.names( ):
      if name in [ "container", "config" ]:
         continue

      for value in umbs.configuration.values( name ):
         if "root_dir" == name:
            value = umbs.configuration.value( 'container_root_dir' )

         cfg.write( f"{name}:         {value}\n" )
   cfg.close( )



   container_root_dir = umbs.configuration.value( 'container_root_dir' )
   container_umbs_dir = os.path.join( container_root_dir, "umbs" )
   container_pfw_dir = os.path.join( container_root_dir, "pfw" )

   container_name = umbs.configuration.value( 'container_name' )
   user_name = umbs.configuration.value( 'container_user_name' )
   image_name = umbs.configuration.value( 'image_name' )
   image_tag = umbs.configuration.value( 'image_tag' )
   volume_mapping = [
         pfw.linux.docker.container.Mapping( host =  umbs.configuration.value( 'root_dir' ), guest =  container_root_dir ),
         pfw.linux.docker.container.Mapping( host =  umbs.configuration.value( 'umbs' ), guest =  f"{container_umbs_dir}" ),
         pfw.linux.docker.container.Mapping( host =  umbs.configuration.value( 'pfw' ), guest =  f"{container_pfw_dir}" ),
         pfw.linux.docker.container.Mapping( host = f"~/.ssh", guest = f"/home/{user_name}/.ssh" ),
         pfw.linux.docker.container.Mapping( host = f"~/.gitconfig", guest = f"/home/{user_name}/.gitconfig" ),
      ]
   port_mapping = [
         pfw.linux.docker.container.Mapping( host = "5000", guest = "5000" ),
      ]
   workdir = container_umbs_dir

   container_project = umbs.configuration.value( 'project' )
   container_action = umbs.configuration.value( 'action' )

   command = f"python3 {container_umbs_dir}/umbs.py"
   command += f" --config={container_umbs_dir}/{cfg_file}"
   command += f" --pfw={container_pfw_dir}"
   command += f" --project={container_project}"
   command += f" --action={container_action}"
   # command = ""

   pfw.linux.docker.container.run( container_name, f"{image_name}:{image_tag}",
         volume_mapping = volume_mapping,
         port_mapping = port_mapping,
         workdir = workdir,
         disposable = True,
         command = command
      )
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
