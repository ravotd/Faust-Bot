from FaustBot.Modules.ModulePrototype import ModulePrototype
from FaustBot.Modules.ModuleType import ModuleType


class LeaveObserverPrototype(ModulePrototype):
    """
    The Prototype of a Class who can react to every action
    """

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_LEAVE]

    def __init__(self):
        pass

    def update_on_leave(self, data):
        raise NotImplementedError("Some module doesn't do anything")
