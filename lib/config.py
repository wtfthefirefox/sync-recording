import os
import yaml


class RecorderConfig(object):
    def __init__(self):
        self._data = None
        self._secrets = {}

    def __getitem__(self, key):
        self._check_data()
        return self._data[key]

    def _check_data(self):
        if self._data is None:
            raise RuntimeError("Config is not loaded")

    def load_from(self, path):
        with open(path, "r") as yml:
            self._data = yaml.load(yml, Loader=yaml.FullLoader)


config = RecorderConfig()
