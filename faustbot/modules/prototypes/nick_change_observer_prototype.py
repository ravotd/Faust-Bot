from faustbot.modules.module_type import ModuleType
from faustbot.modules.prototypes.module_prototype import ModulePrototype


class NickChangeObserverPrototype(ModulePrototype):
    """
    The Prototype of a Class who can react to every action
    """

    @staticmethod
    def cmd():
        raise NotImplementedError()

    @staticmethod
    def help():
        raise NotImplementedError("Need sto be implemented by subclasses!")

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_NICK_CHANGE]

    def __init__(self):
        super().__init__()

    def update_on_nick_change(self, data, connection):
        raise NotImplementedError("Some module doesn't do anything")
