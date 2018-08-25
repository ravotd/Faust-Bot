from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.module_prototype import ModulePrototype
from faustbot.util import logging


class Observable(object):
    def __init__(self):
        self._observers = []
        self._logger = logging.get_logger(Observable.__name__)

    def add_observer(self, observer):
        self._observers.append(observer)
        self._logger.info("appended" + str(observer.__class__.__name__))

    def get_observer(self):
        return self._observers

    # data has to be a dictionary matching the structure of the query
    def notify_observer(self, observer: ModulePrototype, data: IRCData, connection):
        # here implement some data handling. Fill self._data with the data received
        raise NotImplementedError("Some Observable doesn't know what to do with its input data")

    def input(self, data: IRCData, connection):
        # here implement some data handling. Fill self._data with the data received
        channel = data.channel
        blacklist = None
        if data.is_channel():
            blacklist = connection.config.get_channel_by_name(channel).blacklist
        else:
            blacklist = []
        for observer in self._observers:
            if data.is_channel() and observer.is_channel_only():
                continue
            if observer.__class__.__name__ not in blacklist:
                self.notify_observer(observer, data, connection)
            else:
                self._logger.debug('%s is blacklisted for %s, message %s not redirected' % (observer.__class__.__name__,
                                                                                            channel, data.message))

    def rm_observer(self, observer):
        self._observers.remove(observer)

    # if module.__class__.__name__ in self._config.blacklist:
    #    print(module.__class__.__name__ + " not loaded because of blacklisting")
    #    return
