import os
import platform
import ConfigParser
from django.conf import settings

def write_config(config, section, config_dict=None, **kwargs):
    config.add_section(section)
    if config_dict:
        for key in config_dict:
            config.set(section, key, config_dict[key])

    for key in kwargs:
        config.set(section, key, kwargs[key])
    print '========================================'

def django_manage(args):
    cmd = 'python ./manage.py ' + args
    os.system(cmd)

def get_config(section, option, filename='NTHUFC.cfg'):
    '''Return a config in that section'''
    try:
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        if(platform.system() == 'Windows'):
            config.read(settings.BASE_DIR + '\\NTHUFC\\config\\' + filename)
        else:
            config.read(settings.BASE_DIR + '/NTHUFC/config/' + filename)
        return config.get(section, option)
    except:
        # no config found
        return None
