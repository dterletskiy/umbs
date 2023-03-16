#!/usr/bin/python


import pfw.console
import pfw.shell
import pfw.base.str
import pfw.base.dict
import pfw.linux.password

import configuration
import docker.image
import docker.container
import docker.packages.ubuntu

def docker( ):
   dockerfile = configuration.value( "dockerfile" )

   os_name = configuration.value( "docker_os_name" )
   os_version = configuration.value( "docker_os_version" )
   image_name = configuration.value( "docker_image_name" )
   image_tag = configuration.value( "docker_image_tag" ) # datetime.datetime.now( ).strftime( "%Y.%m.%d_%H.%M.%S" )
   user_id = 1000
   user_gid = 1000
   user_name = configuration.value( "docker_user_name" )
   user_password = configuration.value( "docker_user_password" )
   user_password_salt = configuration.value( "docker_user_password_salt" )
   user_hashed_password = pfw.linux.password.build_hashed_password( user_password, user_password_salt )
   user_workdir = configuration.value( "docker_user_workdir" )
   container_name = configuration.value( "docker_container_name" )
   packages = " ".join( docker.packages.ubuntu.packages_all )
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



   docker.image.build(
         dokerfile = dockerfile,
         image_name = image_name,
         image_tag = image_tag,
         build_args = build_args
      )

   docker.container.run(
         container_name = container_name,
         image_name = image_name,
         image_tag = image_tag,
         volume_mapping = volume_mapping,
         port_mapping = port_mapping
      )
# def docker
