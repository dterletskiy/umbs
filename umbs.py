#!/usr/bin/python

# Examples:
# 
# CONFIG=./configuration.cfg
# PFW=/mnt/dev/repos/github.com/dterletskiy/python_fw
# RPOJECT="u-boot"
# ACTION=build
# 
# 
# 
# ./main.py --config=./${CONFIG} --include=${PFW} --project=${RPOJECT} --action=${ACTION}
# ./main.py --config=./${CONFIG} --project=${RPOJECT} --action=${ACTION}
# 
# In case if variable "INCLUDE" defined with path to "pfw" "--include" option could be omitted.
# If "INCLUDE" variable defined several times in configuration file all mentioned values will be used.



import sys

import umbs.configuration



##########################################################################
#                                                                        #
#                          Begin configuration                           #
#                                                                        #
##########################################################################

def init( ):
   MIN_PYTHON = (3, 8)
   if sys.version_info < MIN_PYTHON:
      print( "Python minimal required version is %s.%s" % MIN_PYTHON )
      print( "Current version is %s.%s" % ( sys.version_info.major, sys.version_info.minor ) )
      sys.exit( 255 )

   umbs.configuration.configure( sys.argv[1:] )
   umbs.configuration.info( ) # @TDA: debug
# def init

init( )

##########################################################################
#                                                                        #
#                           End configuration                            #
#                                                                        #
##########################################################################



import umbs.main



def main( ):
   umbs.main.main( )

if __name__ == "__main__":
   main( )



# import pfw.linux.archive

# source_original = "/mnt/dev/tmp/archive/data/"
# source_unpacked = "/mnt/dev/tmp/archive/000/"
# archive = "/mnt/dev/tmp/archive/archive.tar.gz"
# format = "tar.gz"

# pfw.linux.archive.pack( archive, format, "./data/", directory = "/mnt/dev/tmp/archive/" )
# pfw.linux.archive.unpack( archive, source_unpacked, format )
# # pfw.linux.archive.detect_type( archive )
