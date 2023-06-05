#!/usr/bin/python3

import pfw.console
import pfw.shell
import pfw.linux.docker2



def build( **kwargs ):
   kw_dockerfile = kwargs.get( "dockerfile", None )
   kw_image_name = kwargs.get( "image_name", None )
   kw_image_tag = kwargs.get( "image_tag", None )
   kw_build_args = kwargs.get( "build_args", [ ] )

   pfw.linux.docker2.build(
         dokerfile = kw_dockerfile,
         image_name = kw_image_name,
         image_tag = kw_image_tag,
         build_args = kw_build_args
      )
# def build

