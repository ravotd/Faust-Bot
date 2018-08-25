import _thread

from faustbot.communication.observable import Observable
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.notice_observer_prototype import NoticeObserverPrototype


class NoticeObservable(Observable):
    def notify_observer(self, observer: NoticeObserverPrototype, data: IRCData, connection):
        _thread.start_new_thread(observer.__class__.update_on_notice, (observer, data, connection))
