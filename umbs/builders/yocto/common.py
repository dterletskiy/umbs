import os

import pfw.console
import pfw.shell

import umbs.builders.base



def get_instance( config, **kwargs ):
   return Actor( config, **kwargs )
# def get_instance



class Actor( umbs.builders.base.Actor ):
   def __init__( self, config, **kwargs ):
      super( ).__init__( config, **kwargs )

      strict_fields = [ "target" ]
      for key in strict_fields:
         if key not in self.__config:
            raise umbs.base.YamlFormatError( f"Filed '{key}' must be defined in builder" )

      self.__target = self.__config["target"]
      self.__layers = [ os.path.join( self.__component_dir, i ) for i in self.__config.get( "layers", [ ] ) ]
   # def __init__

   def config( self, **kwargs ):
      command = f""
      return 0 == self.__execute( command )["code"]
   # def config

   def build( self, **kwargs ):
      command = f"bitbake"
      command += f" --verbose"
      command += f" {self.__target}"
      return 0 == self.__execute( command )["code"]
   # def build

   def clean( self, **kwargs ):
      return True
   # def clean

   def __execute( self, command ):
      cmd = f"source oe-init-build-env {self.__product_dir}"
      for layer in self.__layers:
         cmd += f" && {layer}"
      if command and 0 < len( command ):
         cmd += f" && {command}"
      return self.execute( cmd )
   # def __execute
# class Actor





# CURRENT_DIR=${PWD}
# ROOT_DIR="/mnt/docker/builder/yocto"
# BUILD_DIR="${ROOT_DIR}/build/"
# POKY_DIR="${ROOT_DIR}/poky/"

# POKY_URL="git://git.yoctoproject.org/poky"
# POKY_BRANCH="mickledore"
# POKY_DEPTH=1

# TARGET="core-image-minimal"
# TASK="do_compile"


# cd ${ROOT_DIR}
# git clone --branch ${POKY_BRANCH} --depth ${POKY_DEPTH} ${POKY_URL} ${POKY_DIR}

# source "${POKY_DIR}/oe-init-build-env" ${BUILD_DIR}
# # bitbake-layers create-layer ${TDA_LAYER_DIR}
# bitbake-layers add-layer ${TDA_LAYER_DIR}
# bitbake --verbose ${TARGET}
