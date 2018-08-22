from faustbot.communication import connection
from faustbot.modules.module_type import ModuleType
from faustbot.modules.prototypes.module_prototype import ModulePrototype


class NoticeObserverPrototype(ModulePrototype):
    @staticmethod
    def cmd():
        raise NotImplementedError()

    @staticmethod
    def help():
        raise NotImplementedError("Need sto be implemented by subclasses!")

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_NOTICE]

    def __init__(self):
        super().__init__()

    def update_on_notice(self, data, connection: connection):
        raise NotImplementedError('Needs to be implemented by csubclasses!')
