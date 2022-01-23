from configparser import ConfigParser
from hashlib import sha256
import psycopg2


def config(filename='database-local.ini', section='postgresql'):
    """This function was *wholly* copied from someone else, thanks them"""
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    connection = psycopg2.connect(**db)
    return connection


def passEncryption(plainTextPass):
    bytedPass = plainTextPass.encode()
    shaSignLong = sha256(bytedPass)
    shaSign = shaSignLong.hexdigest()
    return shaSign
