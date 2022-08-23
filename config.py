import configparser
configfile = 'config.ini'

def read_config():
    config = configparser.RawConfigParser()
    config.optionxform = lambda option: option
    config.read(configfile)
    config_dict = _copy_config_from_parser(config)

    return config_dict, config

def _split_config_entry(e):
    entry = e.split('x')
    entry = (int(entry[0]), int(entry[1]))
    return entry

def _copy_config_from_parser(config_parser):
    config_dict = {'Video': {}, 'FTP': {}}
    for key, value in config_parser['Video'].items():
        if key == 'VideoTimer':
            config_dict['Video'][key] =  int(value)
        else:
            config_dict['Video'][key] = _split_config_entry(value)
    
    for key, value in config_parser['FTP'].items():
        config_dict['FTP'][key] = value

    return config_dict

def save_config(self):
    config_parser = configparser.RawConfigParser()
    config_parser.optionxform = lambda option: option
    config_parser['Video'] = {
            'VideoResolution': str(self.video_resolution_entry.get()),
            'ImageResolution': str(self.image_resolution_entry.get()),
            'PreviewResolution': str(self.preview_resolution_entry.get()),
            'VideoTimer': str(self.video_timer_entry.get())
    }
    config_parser['FTP'] = {
            'Host': str(self.ftp_host_entry.get()),
            'User': str(self.ftp_user_entry.get()),
            'Password': str(self.ftp_password_entry.get())
    }
    with open(configfile, 'w') as c:
        config_parser.write(c)
    
    self.config = _copy_config_from_parser(config_parser)
