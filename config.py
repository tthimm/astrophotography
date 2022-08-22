import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['DEFAULT']
    conf = {}
    conf['VideoResolution'] = split_config_entry(config['VideoResolution'])
    conf['ImageResolution'] = split_config_entry(config['ImageResolution'])
    conf['PreviewResolution'] = split_config_entry(config['PreviewResolution'])
    conf['VideoTimer'] = int(config['VideoTimer'])
    return conf

def split_config_entry(e):
    entry = e.split('x')
    entry = (int(entry[0]), int(entry[1]))
    return entry
