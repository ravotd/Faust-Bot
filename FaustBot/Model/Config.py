class Config(object):
    CONFIG_PATH = 'config_path'

    def __init__(self, path=None):
        """

        :param path:
        """
        self._config_dict = {}
        if path:
            self._config_dict[Config.CONFIG_PATH] = path
            self.read_config(path)

    def __getitem__(self, item: str):
        if item in self._config_dict:
            return self._config_dict[item]
        else:
            return None

    def __setitem__(self, key: str, value: str):
        self._config_dict[key] = value

    def read_config(self, path: str, append=True):
        f = open(path, 'r')
        if not append:
            self._config_dict = {}
        for l in f.readlines():
            kv_pair = l.split(':')
            if len(kv_pair) == 2:
                self._config_dict[kv_pair[0].strip()] = kv_pair[1][:-1].strip()

    @property
    def lang(self):
        return self._config_dict["lang"]

    @lang.setter
    def lang(self, value):
        self._config_dict["lang"] = value

    @property
    def mods(self):
        return self._config_dict["mods"]

    @mods.setter
    def mods(self, value):
        self._config_dict["mods"] = value
