# ./libCommon.py
from glob import glob
from json import dumps, load, loads
from os import path, environ, remove, stat, mkdir as MKDIR
import logging
import pandas as PD
from sys import version_info
from time import time, sleep
from traceback import print_exc

try :
   if version_info.major ==3 :
       from configparser import RawConfigParser as CF
   else:
      from ConfigParser import RawConfigParser as CF
except :
    print_exc()
if version_info < (3, 0):
   import ConfigParser
else:
    import configparser as ConfigParser
      
LOG_FORMAT_TEST = '%(levelname)s [%(module)s.%(funcName)s:%(lineno)d] %(message)s'
LOG_FORMAT_APP = '[%(asctime)] %(levelname)s [%(module)s.%(funcName)s:%(lineno)d] %(message)s'
LOG_FORMAT_DATE = "%Y%m%dT%"
LOG = logging.getLogger(__name__) 

def find_files(path_name) :
    return glob('{}*'.format(str(path_name).strip('*')))
def remove_file(filename) :
    if not path.exists(filename) : return
    remove(filename)
def mkdir(pathname) :
    if pathname is None : 
         raise ValueError("Object is null")
    if path.exists(pathname):
       LOG.info('Already exists {}'.format(pathname))
       return
    LOG.info('Creating directory {}'.format(pathname))
    MKDIR(pathname)
def load_environ() :
     return { key : environ[key] for key in environ if is_environ(key) }
def is_environ(arg) :
    if 'SUDO' in arg : return True
    if 'NAME' in arg : return True
    if 'USER' in arg : return True
    if 'PATH' in arg : return True
    if 'PWD' in arg : return True
    if 'HOME' in arg : return True
    return False  
def pretty_print(obj) :
    _xx = transform_obj(obj)
    if isinstance(_xx,(float, int, str, tuple)) : 
        return _xx
    if isinstance(_xx,(list)) : 
        return dumps( _xx , indent=3, sort_keys=True)
    _yy = { key : _xx[key] for key in _xx if not is_json_enabled(_xx[key]) }

    ret = { key : _xx[key] for key in _xx if is_json_enabled(_xx[key]) }
    ret.update( { key : str(_yy[key]) for key in _yy if hasattr(_yy[key],'__str__') } )
    ret.update( { key : str(type(_yy[key])) for key in _yy if not hasattr(_yy[key],'__str__') } )
    return dumps( transform_obj(obj)  , indent=3, sort_keys=True)
def is_json_enabled(obj) :
    try :
        dumps(obj)
        return True
    except : pass
    return False
def transform_obj(obj) :
    if obj is None :
        raise ValueError('Object is None')
    if isinstance(obj,(float, int, str, dict, tuple)) : 
        return obj
    if isinstance(obj,list) :
        return [ transform_obj(arg) for arg in obj if is_str(arg) ]
    if hasattr(obj,'sections') and hasattr(obj,'items') :
       return { section : { key : value for (key,value) in obj.items(section) } for section in obj.sections() }
    prop_list = [ key for key in dir(obj) if not key.startswith("__") and _build_arg(getattr(obj,key)) ]
    return { key : transform_object(getattr(obj,key))  for key in prop_list }
def build_args(*largs) :
    return "".join( [ str(arg).strip(' ') for arg in largs if is_str(arg) ] )
def build_path(*largs) :
    return "/".join( [ str(arg).strip('/') for arg in largs if is_str(arg) ] )
def build_command(*largs) :
    return " ".join( [ str(arg).strip(' ') for arg in largs if is_str(arg) ] )
def is_str(arg) :
    if arg is None : return False
    if callable(arg) : return False
    if hasattr(arg,'__str__') : return True
    return True
def find_subset(obj,*largs) :
    if obj is None :
       raise ValueError("obj is NoneType")
    if isinstance(obj, dict) :
       return { key: obj[key] for key in largs if key in obj }
    if isinstance(obj,PD.DataFrame) :
        columns = obj.columns.values.tolist()
        omit = { key for key in columns if key not in largs }
        ret = obj.drop(omit,axis=1)
        return ret
    return { key : getattr(obj,key) for key in largs if key in hasattr(obj.key) }
def load_config(fileName) :
    config = CF()
    config.read(fileName)
    return transform_obj(config)
def load_json(fileName) :
    with open(glob(fileName)[0]) as fp :
        return load(fp)
