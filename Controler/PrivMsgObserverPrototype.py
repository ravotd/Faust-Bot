class PrivMsgObserverPrototype(object):
    """
    The Prototype of a Class who can react to every action
    """

    def __init__(self):
        pass

    def update_on_priv_msg(self, data):
        raise NotImplementedError("Some module doesn't do anything")
