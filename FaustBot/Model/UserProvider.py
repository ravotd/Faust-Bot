import sqlite3
import time
from typing import Union


class UserProvider(object):
    """
    Provides information about the users
    """

    def __init__(self):
        self.database_connection = sqlite3.connect('faust_bot.db')
        cursor = self.database_connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER  PRIMARY KEY , name TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS user_stats(id INTEGER  PRIMARY KEY, characters INT, channel TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS last_seen (id INTEGER  PRIMARY KEY, last_seen REAL, channel TEXT)')
        self.database_connection.commit()

    def get_characters(self, name: str, channel: str) -> int:
        """
        :param name: name of user whom characters are to get
        :return: total number of characters written
        """
        cursor = self.database_connection.cursor()
        id = self._get_id(name)
        if id is None:
            return 0
        for characters in cursor.execute("SELECT characters FROM user_stats WHERE id = ? AND channel = ?",
                                         (id, channel)):
            return characters[0]
        return 0

    def get_activity(self, name: str, channel: str) -> float:
        """
        :param channel:
        :param name: name of user whom activity to get
        :return: last activity by user
        """
        cursor = self.database_connection.cursor()
        id = self._get_id(name)
        if id is None:
            return 0
        for time in cursor.execute("SELECT last_seen FROM last_seen WHERE id = ? AND channel = ?", (id, channel)):
            return time[0]
        return 0

    def add_characters(self, name: str, number: int, channel: str):
        """

        :param channel:
        :param name: User to Add Characters to
        :param number: Number of Characters to add
        :return: nothing
        """
        cursor = self.database_connection.cursor()
        id = self._get_id(name)
        if id is None:
            self._create_user(name, channel)
            id = self._get_id(name)
        for chars in cursor.execute("SELECT characters FROM user_stats WHERE id = ? AND channel = ?", (id, channel)):
            chars = chars[0]
            chars += number
            cursor.execute("UPDATE user_stats SET characters = ? WHERE id = ? AND channel = ?", (chars, id, channel))
            self.database_connection.commit()

    def set_active(self, name: str, channel: str):
        """

        :param channel:
        :param name: set this user active at the moment
        :return: Nothing
        """
        cursor = self.database_connection.cursor()
        id = self._get_id(name)
        ntime = time.time()
        if id is None:
            self._create_user(name, channel)
            id = self._get_id(name)
        cursor.execute("UPDATE last_seen SET last_seen = ? WHERE id = ? AND channel = ? ", (ntime, id, channel))
        self.database_connection.commit()

    def _get_id(self, name: str) -> Union[int, object]:
        cursor = self.database_connection.cursor()
        try:
            for id in cursor.execute("SELECT id FROM user WHERE name = ?", (name,)):
                return id[0]
        except:
            return None

    def _create_user(self, name: str, channel: str):
        cursor = self.database_connection.cursor()
        cursor.execute("INSERT INTO user(name) VALUES (?)", (name,))
        id = self._get_id(name)
        cursor.execute("INSERT INTO user_stats(id, characters, channel) VALUES (?, 0, ?)", (id, channel))
        cursor.execute("INSERT INTO last_seen (id, last_seen, channel) VALUES (?, 0, ?)", (id, channel))
        self.database_connection.commit()

    def __exit__(self, exc_type, exc_value, traceback):
        self.database_connection.close()
