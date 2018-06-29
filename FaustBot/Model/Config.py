import json


class Config(object):
    CONFIG_PATH = 'config_path'

    def __init__(self, path):
        '''

        :param path:
        '''
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
            self._config_dict = {Config.CONFIG_PATH: path}
        cfg = ' '.join(f.readlines())
        cfg = json.loads(cfg)
        self._config_dict.update(cfg)
        channel = self._config_dict['channel']
        self._config_dict['channel'] = []
        for c in channel:
            self._config_dict['channel'].append(ChannelConfig(c))

    # <editor-fold name=Properties>

    @property
    def port(self):
        return self._config_dict['port']

    @port.setter
    def port(self, value: int):
        self._config_dict['port'] = value

    @property
    def nick(self):
        return self._config_dict['nick']

    @nick.setter
    def nick(self, value: str):
        self._config_dict['nick'] = value

    @property
    def server(self):
        return self._config_dict['server']

    @server.setter
    def server(self, value: str):
        self._config_dict['server'] = value

    @property
    def channel(self):
        return self._config_dict['channel']

    @channel.setter
    def channel(self, value: list):
        self._config_dict['channel'] = value
    # </editor-fold>


class ChannelConfig(object):

    def __init__(self, channel: dict, raw: bool = False):
        if channel:
            if raw:
                self._config_dict = {}
                self._read_channel(channel)
            else:
                self._config_dict = channel
        else:
            self._config_dict = {}

    def __getitem__(self, item):
        return self._config_dict[item]

    def __setitem__(self, key, value):
        self._config_dict[key] = value

    def _read_channel(self, channel_dict: dict):
        mods = channel_dict['mods']
        self._config_dict['mods'] = []
        for mod in mods:
            self._config_dict['mods'].append(mod.strip())
        if len(mods) > 0:
            del channel_dict['mods']
        # If no idle_time value is given, we set it to five hours ( == 18000 seconds )
        if 'idle_time' not in channel_dict:
            self._config_dict['idle_time'] = 18000
        else:
            self._config_dict['idle_time'] = int(channel_dict['idle_time'])
            del channel_dict['idle_time']
        if 'blacklist' not in channel_dict:
            self._config_dict['blacklist'] = []
        else:
            blacklist = channel_dict['blacklist']
            self._config_dict['blacklist'] = []
            for module in blacklist:
                self._config_dict['blacklist'].append(module.strip())
            if len(blacklist) > 0:
                del channel_dict['blacklist']
        self._config_dict.update(channel_dict)

    # <editor-fold name=Properties>
    @property
    def name(self):
        return self._config_dict['name']

    @name.setter
    def name(self, value: str):
        self._config_dict['name'] = value

    @property
    def group(self):
        return self._config_dict['group']

    @group.setter
    def group(self, value: str):
        self._config_dict['group'] = value

    @property
    def lang(self):
        return self._config_dict['lang']

    @lang.setter
    def lang(self, value: str):
        self._config_dict['lang'] = value

    @property
    def mods(self):
        return self._config_dict['mods']

    @mods.setter
    def mods(self, value: list):
        self._config_dict['mods'] = value

    @property
    def idle_time(self):
        return self._config_dict['idle_time']

    @idle_time.setter
    def idle_time(self, value: int):
        self._config_dict['idle_time'] = value

    @property
    def blacklist(self):
        return self._config_dict['blacklist']

    @blacklist.setter
    def blacklist(self, value: list):
        self.blacklist = value
    # </editor-fold>
