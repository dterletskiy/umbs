import os
import sys
import copy
import re

import pfw.base.dict



globals( )[ "root" ] = { }
globals( )[ "components" ] = { }

def get_value( keys, default_value = None, **kwargs ):
   return pfw.base.dict.get_value( globals( ), keys, default_value, **kwargs )
# def get_value
