from FaustBot.Communication import Connection
from FaustBot.Model.Introduction import IntroductionProvider
from FaustBot.Modules import UserList
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class IntroductionObserver(PrivMsgObserverPrototype):
    def __init__(self, user_list: UserList):
        super().__init__()
        self.userList = user_list

    @staticmethod
    def cmd():
        return [".me"]

    @staticmethod
    def help():
        return ".me - kann von registrierten Nutzern verwendet werden um eine Vorstellung zu speichern00"

    @staticmethod
    def is_valid_me_command(message: str):
        return message == '.me' or message == '.me-'

    def update_on_priv_msg(self, data, connection: Connection):
        # The .me command should be only available within a channel
        command = data.message.split(' ')[0]
        if not IntroductionObserver.is_valid_me_command(command) or data.is_query():
            return
        if not self.authenticated(data.nick, data.channel, connection):
            connection.send_back("Für die Nutzung von .me ist es zwingend erforderlich, einen registrierten Nick zu "
                                 "haben sowie eingeloggt zu sein. Wie dies geht, erfährst du unter "
                                 "https://autistenchat.org/#clients", data)
            return
        intro_provider = IntroductionProvider()
        payload = data.message.split('.me')[1].strip()
        if len(payload) == 0:
            text = IntroductionObserver.get_existing_me(data, intro_provider)
        elif len(payload) == 1 and '-' in payload:
            intro_provider.delete_intro(data.nick, data.channel)
            text = data.nick + " dein Intro wurde gelöscht!", data
        else:
            text = IntroductionObserver.save_or_replace(data, payload, intro_provider)
            connection.send_back(text, data)
            text = IntroductionObserver.get_existing_me(data, intro_provider)
        connection.send_back(text, data)

    def authenticated(self, nick: str, channel: str, connection: Connection):
        channel_users = self.userList.userList.get(channel)
        if channel_users is None or nick not in channel_users:
            return False
        return connection.is_identified(nick)

    @staticmethod
    def save_or_replace(data, payload, intro_provider):
        intro_provider.save_or_replace(data.nick, payload, data.channel)
        text = ": Dein Intro wurde gespeichert! Mittels .me- kannst du deinen Eintrag wieder löschen."
        return data.nick + text

    @staticmethod
    def get_existing_me(data, intro_provider):
        intro = intro_provider.get_intro(data.nick, data.channel)
        if intro is not None:
            text = " ist " + intro[1]
        else:
            text = " für dich gibt es noch keinen Eintrag, vielleicht magst du ja mittels .me <intro> noch " \
                   " einen hinzufügen? "
        return data.nick + text


