import os
import sys

import pfw.console
import pfw.shell

import umbs.base
import umbs.configuration
import umbs.docker.main
import umbs.projects.main
import umbs.tools.main






def init_projects( yaml_config ):
   projects_map: dict = { }
   for name in yaml_config.get_projects( ):
      if project := umbs.projects.main.Project( name, yaml_config.get_project( name ), yaml_config.get_variable( "DIRECTORIES.ROOT" ) ):
         projects_map[ name ] = project

   return projects_map
# def init_projects

def init_tools( yaml_config ):
   tools_map: dict = { }
   for name in yaml_config.get_tools( ):
      if tool := umbs.tools.main.Tool( name, yaml_config.get_tool( name ), yaml_config.get_variable( "DIRECTORIES.ROOT" ) ):
         tools_map[ name ] = tool

   return tools_map
# def init_tools



yaml_config: umbs.base.Config = umbs.base.Config( umbs.configuration.value( "yaml_config" ) )
yaml_config.info( )


umbs_projects: dict = init_projects( yaml_config )
umbs_tools: dict = init_tools( yaml_config )



def main( ):
   pfw.console.debug.ok( "------------------------- BEGIN -------------------------" )

   project = umbs.configuration.value( "project" )
   action = umbs.configuration.value( "action" )

   if "docker" == project:
      umbs.docker.main.do_action( action )
   elif "*" == project:
      for name, project in umbs_projects.items( ):
         project.do_action( action )
   else:
      umbs_projects[ project ].do_action( action )

   pfw.console.debug.ok( "-------------------------- END --------------------------" )
# def main
