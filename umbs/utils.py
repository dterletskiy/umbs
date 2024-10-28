import os
import sys
import re

import pfw.size



def string_to_size( string, **kwargs ):
   match = re.match( r'(\d+[.]?\d*)\s*(\w+)', string )
   if not match:
      pfw.console.debug.error( f"format error" )
      return None

   size = float( match.group( 1 ) )
   granularity = pfw.size.text_to_size( match.group( 2 ) )

   if not granularity:
      pfw.console.debug.error( f"dimention error" )
      return None

   return pfw.size.Size( size, granularity )

# def string_to_size
