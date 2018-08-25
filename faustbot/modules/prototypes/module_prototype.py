from faustbot.model.config import Config


class ModulePrototype(object):
    @staticmethod
    def cmd():
        raise NotImplementedError()

    @staticmethod
    def get_module_types():
        raise NotImplementedError("This method needs to be implemented by a subclass!")

    @staticmethod
    def is_channel_only():
        return True

    @staticmethod
    def help():
        raise NotImplementedError("Needs to be implemented by subclasses")

    def __init__(self):
        self._config = None

    @property
    def config(self) -> Config:
        return self._config

    @config.setter
    def config(self, value):
        self._config = value
