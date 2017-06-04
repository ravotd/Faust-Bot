class ModulePrototype(object):
    @staticmethod
    def get_module_types():
        raise NotImplementedError("This method needs to be implemented by a subclass!")

    def __init__(self):
        self._config = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value
