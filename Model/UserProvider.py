class UserProvider(object):
    """
    Provides information about the users
    """
    def get_characters(self, name):
        """

        :param name: name of user whom characters are to get
        :return: total number of characters written
        """
        return 2500

    def get_activity(self, name):
        """

        :param name: name of user whom activity to get
        :return: last activity by user
        """
        return 0

    def add_characters(self, name, number):
        """

        :param name: User to Add Characters to
        :param number: Number of Characters to add
        :return: nothing
        """

    def set_active(self, name):
        """

        :param name: set this user active at the moment
        :return: Nothing
        """

    def permission(self, user, percent):
        """

        :param user: user to ask permission for
        :param percent: percent needed for permission
        :return: True or False
        http://stackoverflow.com/questions/1682920/determine-if-a-user-is-idented-on-irc
        """
        return True
