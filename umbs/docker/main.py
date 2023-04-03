#!/usr/bin/python


import pfw.console
import pfw.shell
import pfw.base.str
import pfw.base.dict
import pfw.linux.password

import umbs.configuration
import umbs.docker.image
import umbs.docker.container
import umbs.docker.packages.ubuntu



def do_action( action ):
   dockerfile = umbs.configuration.value( "dockerfile" )

   os_name = umbs.configuration.value( "docker_os_name" )
   os_version = umbs.configuration.value( "docker_os_version" )
   image_name = umbs.configuration.value( "docker_image_name" )
   image_tag = umbs.configuration.value( "docker_image_tag" ) # datetime.datetime.now( ).strftime( "%Y.%m.%d_%H.%M.%S" )
   user_id = 1000
   user_gid = 1000
   user_name = umbs.configuration.value( "docker_user_name" )
   user_password = umbs.configuration.value( "docker_user_password" )
   user_password_salt = umbs.configuration.value( "docker_user_password_salt" )
   user_hashed_password = pfw.linux.password.build_hashed_password( user_password, user_password_salt )
   user_workdir = umbs.configuration.value( "docker_user_workdir" )
   container_name = umbs.configuration.value( "docker_container_name" )
   packages = " ".join( umbs.docker.packages.ubuntu.packages_all )
   build_args = [
         f"ARG_OS_NAME={os_name}",
         f"ARG_OS_VERSION={os_version}",
         f"ARG_USER_ID={user_id}",
         f"ARG_USER_GID={user_gid}",
         f"ARG_USER_NAME={user_name}",
         # f"ARG_USER_PASSWORD={user_password}",
         # f"ARG_USER_PASSWORD_SALT={user_password_salt}",
         # f"ARG_USER_HASHED_PASSWORD={user_hashed_password}",
         f"ARG_PACKAGES='{packages}'",
         f"ARG_USER_WORKDIR='{user_workdir}'",
      ]

   volume_mapping = [
         pfw.linux.docker.Container.Mapping( host = f"/mnt/docker/{container_name}", guest = f"/mnt/host" ),
         pfw.linux.docker.Container.Mapping( host = f"~/.ssh", guest = f"/home/{user_name}/.ssh" ),
         pfw.linux.docker.Container.Mapping( host = f"~/.gitconfig", guest = f"/home/{user_name}/.gitconfig" ),
      ]

   port_mapping = [
         pfw.linux.docker.Container.Mapping( host = "5000", guest = "5000" ),
      ]



   if "build" == action:
      umbs.docker.image.build(
            dockerfile = dockerfile,
            build_args = build_args,
            image_name = image_name,
            image_tag = image_tag,
         )
   elif "create" == action:
      umbs.docker.container.create(
            container_name = container_name,
            image_name = image_name,
            image_tag = image_tag,
            volume_mapping = volume_mapping,
            port_mapping = port_mapping,
         )
   elif "remove" == action:
      umbs.docker.container.remove(
            container_name = container_name,
         )
   elif "start" == action:
      umbs.docker.container.start(
            container_name = container_name,
         )
   elif "stop" == action:
      umbs.docker.container.stop(
            container_name = container_name,
         )
   elif "run" == action:
      umbs.docker.container.run(
            container_name = container_name,
            image_name = image_name,
            image_tag = image_tag,
            volume_mapping = volume_mapping,
            port_mapping = port_mapping,
         )
   elif "exec" == action:
      umbs.docker.container.exec(
            container_name = container_name,
            image_name = image_name,
            image_tag = image_tag,
            volume_mapping = volume_mapping,
            port_mapping = port_mapping,
         )
   else:
      pfw.console.debug.error( f"Undefined action: '{action}'" )
# def do_action
