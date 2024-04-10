import os
import yaml

from .get_monitors import get_monitors_info


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
            self._data["rooms"] = get_monitors_info(os.path.join(os.getcwd(), self._data["rooms_info_file"]))


config = RecorderConfig()
