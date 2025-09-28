#!/usr/bin/python

# Examples:
# 
# ./umbs.py \
#    --config=./configuration/host.cfg \
#    --component=carpc \
#    --action=fetch \
#    --container=builder_x64_ubuntu_22.04
#
# ./umbs.py \
#    --config=./configuration/host.cfg \
#    --component=carpc \
#    --action=fetch \
#    --container_from=builder/x64/ubuntu:22.04
#
# ./umbs.py \
#    --config=./configuration/guest.cfg \
#    --component=carpc \
#    --action=fetch
# 
# In case if variable "INCLUDE" defined with path to "pfw" "--include" option could be omitted.
# If "INCLUDE" variable defined several times in configuration file all mentioned values will be used.



import umbs.configuration

umbs.configuration.init( verbose = True )



import umbs.main

def main( ):
   umbs.main.main( )

if __name__ == "__main__":
   main( )
