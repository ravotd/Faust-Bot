from FaustBot.Communication.Connection import Connection
from FaustBot.Model.Config import Config
from FaustBot.Model.ConnectionDetails import ConnectionDetails
from FaustBot.Modules import ActivityObserver, IdentNickServObserver, GiveCookieObserver
from FaustBot.Modules import Kicker
from FaustBot.Modules import ModulePrototype
from FaustBot.Modules import PingAnswerObserver
from FaustBot.Modules import SeenObserver
from FaustBot.Modules import TitleObserver
from FaustBot.Modules import UserList
from FaustBot.Modules import WikiObserver
from FaustBot.Modules.CustomUserModules import GlossaryModule
from FaustBot.Modules.CustomUserModules import ICDObserver
from FaustBot.Modules.CustomUserModules import ModmailObserver
from FaustBot.Modules.GiveDrinkObserver import GiveDrinkObserver
from FaustBot.Modules.ModuleType import ModuleType


class FaustBot(object):
    def __init__(self, config_path: str):
        self._config = Config(config_path)
        connection_details = ConnectionDetails(self.config)
        self._connection = Connection(connection_details)

    @property
    def config(self):
        return self._config

    def _setup(self):
        self._connection.establish()
        user_list = UserList.UserList()
        activity = ActivityObserver.ActivityObserver()
        self._connection.receive()
        data = self._connection.last_data()
        while -1 is data.find('353'):  # 353 RPL_NAMREPLY
            self._connection.receive()
            data = self._connection.last_data()
            print(data)
        self.add_module(user_list)
        self.add_module(activity)
        # self._connection._join.input_names(data)

        self.add_module(user_list)
        self.add_module(user_list)
        self.add_module(user_list)
        self.add_module(activity)
        self.add_module(PingAnswerObserver.ModulePing())
        self.add_module(Kicker.Kicker())
        self.add_module(activity)
        self.add_module(SeenObserver.SeenObserver())
        self.add_module(TitleObserver.TitleObserver())
        self.add_module(WikiObserver.WikiObserver())
        self.add_module(ModmailObserver.ModmailObserver())
        self.add_module(ICDObserver.ICDObserver())
        self.add_module(GlossaryModule.GlossaryModule(self._config))
        self.add_module(IdentNickServObserver.IdentNickServObserver())
        self.add_module(GiveDrinkObserver())
        self.add_module(GiveCookieObserver.GiveCookieObserver())

    def run(self):
        self._setup()
        running = True
        while running:
            if not self._connection.receive():
                return

    def add_module(self, module: ModulePrototype):
        for module_type in module.get_module_types():
            observable = self._get_observable_by_module_type(module_type)
            observable.add_observer(module)
        module.config = self._config

    def _get_observable_by_module_type(self, module_type: str):
        if module_type == ModuleType.ON_JOIN:
            return self._connection.join_observable

        if module_type == ModuleType.ON_LEAVE:
            return self._connection.leave_observable

        if module_type == ModuleType.ON_KICK:
            return self._connection.kick_observable

        if module_type == ModuleType.ON_MSG:
            return self._connection.priv_msg_observable

        if module_type == ModuleType.ON_NICK_CHANGE:
            return self._connection.nick_change_observable

        if module_type == ModuleType.ON_PING:
            return self._connection.ping_observable

        if module_type == ModuleType.ON_NOTICE:
            return self._connection.notice_observable
