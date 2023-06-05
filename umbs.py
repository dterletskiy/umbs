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



import umbs.configuration

umbs.configuration.init( )
# umbs.configuration.info( ) # @TDA: debug



import umbs.main

def main( ):
   umbs.main.main( )

if __name__ == "__main__":
   main( )
