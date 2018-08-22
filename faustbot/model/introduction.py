import sqlite3


class IntroductionProvider(object):
    _CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS introduction (id INTEGER PRIMARY KEY, \
                    user TEXT, intro TEXT, channel TEXT)'
    _GET_INTRO = 'SELECT id, intro FROM introduction WHERE user = ? AND channel = ?'
    _SAVE_OR_OVERWRITE = 'REPLACE INTO introduction (id, user, intro, channel) VALUES (?, ?, ?, ?)'
    _DELETE_INTRO = 'DELETE FROM introduction WHERE user = ? AND channel = ?'

    def __init__(self):
        self._database_connection = sqlite3.connect('faust_bot.db')
        cursor = self._database_connection.cursor()
        cursor.execute(IntroductionProvider._CREATE_TABLE)
        self._database_connection.commit()

    def get_intro(self, user: str, channel: str):
        cursor = self._database_connection.cursor()
        cursor.execute(IntroductionProvider._GET_INTRO, (user.lower(), channel.lower()))
        return cursor.fetchone()

    def save_or_replace(self, user: str, intro: str, channel: str):
        existing = self.get_intro(user)
        _id = existing[0] if existing is not None else None
        data = (_id, user.lower(), intro, channel.lower())
        cursor = self._database_connection.cursor()
        cursor.execute(IntroductionProvider._SAVE_OR_OVERWRITE, data)
        self._database_connection.commit()

    def delete_intro(self, user: str, channel: str):
        cursor = self._database_connection.cursor()
        cursor.execute(IntroductionProvider._DELETE_INTRO, (user.lower(), channel.lower()))
        self._database_connection.commit()

    def __exit__(self):
        self._database_connection.close()
