import os
import sys

import pfw.console
import pfw.shell

import umbs.base
import umbs.configuration
import umbs.docker.main
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
   cfg = open( "configuration_gen.cgf", "w" )
   for config in umbs.configuration.config.get_data_list( ):
      skip = False
      for key in [ "container", "config" ]:
         if key == config.get_name( ):
            skip = True
            break
      if skip:
         continue

      for value in config.get_values( ):
         cfg.write( f"{config.get_name( )}:         {value}\n" )
   cfg.close( )
# def run_in_container



def main( ):
   yaml_config: umbs.base.Config = umbs.base.Config( umbs.configuration.value( "yaml_config" ), root_dir = umbs.configuration.value( "root_dir" ) )
   yaml_config.info( )
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
