import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['DEFAULT']
    return config

def split_config_entry(e):
    entry = e.split('x')
    entry = (int(entry[0]), int(entry[1]))
    return entry
