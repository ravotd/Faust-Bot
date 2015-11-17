class ModuleProtoype(object):
    """
    The Prototype of a Class who can react to every action
    """
    def __init__(self):
        pass

    def update(self, data):
        raise NotImplementedError("Some module doesn't do anything")