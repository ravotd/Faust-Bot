from FaustBot.Communication.Connection import Connection
from FaustBot.Model.GlossaryProvider import GlossaryProvider
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class GlossaryModule(PrivMsgObserverPrototype):
    _QUERY_EXPLANATION = '.?'
    _REMOVE_EXPLANATION = '.?-'
    _ADD_EXPLANATION = '.?+'

    def __init__(self):
        super().__init__()

    def update_on_priv_msg(self, data, connection: Connection):
        msg = data['message']
        if not -1 == msg.find(GlossaryModule._REMOVE_EXPLANATION):
            self._remove_query(data, connection)
        elif not -1 == msg.find(GlossaryModule._ADD_EXPLANATION):
            self._add_query(data, connection)
        elif not -1 == msg.find(GlossaryModule._QUERY_EXPLANATION):
            self._answer_query(data, connection)

    def _answer_query(self, data, connection: Connection):
        """
        
        :param data: 
        :param connection: 
        :return: 
        """
        glossary_provider = GlossaryProvider()
        split = data['message'].split(GlossaryModule._QUERY_EXPLANATION)
        if not len(split) == 2:
            return
        answer = glossary_provider.get_explanation(split[1].strip())
        if answer[1] is None or answer[1].strip() == '':
            answer = "Tut mir leid, " + data['nick'] + ". Für " + split[1] + " habe ich noch keine Erklärung."
        connection.send_back(answer[1], data)

    def _remove_query(self, data, connection: Connection):
        """
        
        :param data: 
        :param connection: 
        :return: 
        """
        pass

    def _add_query(self, data, connection: Connection):
        """
        
        :param data: 
        :param connection: 
        :return: 
        """
        if not connection.is_idented(data['nick']):
            connection.send_back("Du du du, das darfst du aber nicht, " + data['nick'] + ".", data)
            return
        msg = data['message'].split(GlossaryModule._ADD_EXPLANATION)[1].strip()

        split = msg.split(' ', 1)
        glossary_provider = GlossaryProvider()
        glossary_provider.save_or_replace(split[0], split[1])
        connection.send_back(data['nick'] + " die Erklärung für " + split[0] + " wurde hinzugefügt.", data)
