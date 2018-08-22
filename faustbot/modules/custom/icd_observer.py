import csv
import re

from faustbot.communication.connection import Connection
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class ICDObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def get_icd(self, code):
        icd10_codes = open('care_icd10_de.csv', 'r',encoding='utf8')
        icd10 = csv.reader(icd10_codes, delimiter=';', quotechar='"')
        for row in icd10:
            if row[0] == code:
                return code +' - ' + row[1]
        return 0

    def update_on_priv_msg(self, data, connection: Connection):
        regex = "(?P<url>https?://[^\s]+)"
        message = re.sub(regex, ' ', data['message'])
        if data['channel'] != connection.config.get_channel():
            return
        regex = r'\b(\w\d{2}\.?\d?)\b'
        codes = re.findall(regex, message)
        for code in codes:
            code = code.capitalize()
            text = self.get_icd(code)
            if text == 0:
                if code.find('.') != -1:
                    code += '-'
                else:
                     code += '.-'
            text = self.get_icd(code)
            if text != 0:
                connection.send_back(text, data)