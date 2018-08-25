import os

from faustbot.communication.connection import Connection
from faustbot.model.config import Config
from faustbot.model.user_list import UserList
from faustbot.modules import activity_observer, ident_nickserv_observer, cookie_observer, who_observer, \
    ping_observer, drink_observer, food_observer, comic_observer, introduction_observer, hangman_observer, \
    duck_observer, all_seen_observer, love_peace_observer, free_hugs_observer, title_observer, wiki_observer, kicker
from faustbot.modules.module_type import ModuleType
from faustbot.modules.prototypes import module_prototype
from faustbot.util.logging import enable_debug_mode, get_logger


class FaustBot(object):
    def __init__(self, config_path: str, debug: bool = False):
        config_path = os.path.join(os.getcwd(), config_path)
        self._config = Config(config_path)
        self._connection = Connection(self._config)
        enable_debug_mode(debug)
        self._logger = get_logger(__name__)
        self._logger.info('Created FaustBot')

    @property
    def config(self):
        return self._config

    def _setup(self):
        self._connection.establish()
        user_list = UserList()
        self.add_module(user_list)
        self.add_module(activity_observer.ActivityObserver())
        self.add_module(who_observer.WhoObserver(user_list))
        self.add_module(all_seen_observer.AllSeenObserver(user_list))
        self.add_module(ping_observer.ModulePing())
        self.add_module(kicker.Kicker(user_list))
        # self.add_module(SeenObserver.SeenObserver())
        self.add_module(title_observer.TitleObserver())
        self.add_module(wiki_observer.WikiObserver())
        # self.add_module(ModmailObserver.ModmailObserver())
        # self.add_module(ICDObserver.ICDObserver())
        # self.add_module(GlossaryModule.GlossaryModule(self._config))
        self.add_module(ident_nickserv_observer.IdentNickServObserver())
        self.add_module(drink_observer.GiveDrinkObserver())
        self.add_module(cookie_observer.GiveCookieObserver())
        self.add_module(love_peace_observer.LoveAndPeaceObserver())
        self.add_module(free_hugs_observer.FreeHugsObserver())
        self.add_module(food_observer.GiveFoodObserver())
        self.add_module(comic_observer.ComicObserver())
        self.add_module(hangman_observer.HangmanObserver())
        # self.add_module(HelpObserver.HelpObserver())
        self.add_module(introduction_observer.IntroductionObserver(user_list))
        self.add_module(duck_observer.DuckObserver())

    def run(self):
        self._setup()
        running = True
        while running:
            if not self._connection.receive():
                return

    def add_module(self, module: module_prototype):
        self._logger.info('loaded module: %s' % module.__class__.__name__)
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

        if module_type == ModuleType.ON_MAGIC_NUMBER:
            return self._connection.magic_number_observable
