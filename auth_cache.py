#!/usr/bin/env python3

import configparser
import settings
from hashlib import md5
import os.path

class auth_cache:

    def __init__(self, username, cache_dir):
        # Set of names of cached paramaters
        parameters = {
            'API_TOKEN', 'API_TOKEN_TIME', 'API_MASK', 'API_COOKIES'
        }
        self.user_config = configparser.ConfigParser()

        # Initialize cache data with empty string.
        self._data = {name: '' for name in parameters}

        # Path to expected cachefile.
        self.cache_path = os.path.normpath(cache_dir) +\
                            os.sep +\
                            md5(username.encode('utf-8')).hexdigest()

        # If cachefile exists - read it and set the parameters
        if os.path.isfile(self.cache_path):
            self.user_config.read(self.cache_path)
            for(parameter, value) in self.user_config['cache'].items():
                self._data[parameter.upper()] = value

    def __getitem__(self, name):
        return self._data[name]

    def __setitem__(self, name, value):
        self._data[name] = value

    def __contains__(self, key):
        return (key in self._data)

    def get_unpacked(self, name):
        return dict([c.split('|') for c in self._data[name].split(',')])\
            if (name in self._data and self._data[name] != '') else dict()

    def set_packed(self, name, value_dict):
        self._data[name] = ','.join([n + '|' + v
                                     for(n, v) in value_dict.items()])

    def write(self):
        self.user_config['cache'] = self._data
        with open(self.cache_path, 'w') as configfile:
            self.user_config.write(configfile)
