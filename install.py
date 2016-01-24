import getpass
import ConfigParser

from func import *

CONFIG_PATH = 'NTHUFC/config/NTHUFC.cfg'

if not os.path.isdir('NTHUFC/config/'):
    print 'Create config dir...',
    os.makedirs('NTHUFC/config')
    print 'done'

if not os.path.isfile(CONFIG_PATH):
    # If the config file does not exist, create one
    print 'Create config file...',
    with open(CONFIG_PATH, 'w') as f:
        f.write('')
    print 'done'

if not os.path.exists('media/'):
    print 'Create media dir...',
    #os.makedirs('media/')
    #os.makedirs('media/uploads/')
    os.makedirs('media/uploads/images')
    print 'done\n'

config = ConfigParser.RawConfigParser()
config.optionxform = str
config.read(CONFIG_PATH)

if not config.has_section('client'):
    # Setting mysql info
    write_config(config, 'client',
        {'default-character-set': 'utf8'},
        host=raw_input('Mysql host: '),
        database=raw_input('Mysql database: '),
        user=raw_input('Mysql user: '),
        password=getpass.getpass('Mysql user password: '),
        email_account=raw_input('Email host acount: '),
        email_password=getpass.getpass('Email host password: '),
    )

# Writing our configuration file
with open(CONFIG_PATH, 'wb') as configfile:
    config.write(configfile)

# Database Migratinos

django_manage('syncdb')

django_manage('makemigrations')
django_manage('migrate')

