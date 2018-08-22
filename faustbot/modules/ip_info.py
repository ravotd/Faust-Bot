# import re
#
# from faustbot.communication.Connection import Connection
# from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
#
#
# class IPInfo(PrivMsgObserverPrototype):
#
#     IP_COMMAND = ".ipinfo"
#     IPV4_RE = r''
#     IPV6_RE = r''
#     URL_RE = r''
#
#
#     @staticmethod
#     def help():
#         return None
#
#     @staticmethod
#     def cmd():
#         return None
#
#     def update_on_priv_msg(self, data, connection: Connection):
#         msg = data['msg']
#         if not msg.startswith(IPInfo.IP_COMMAND):
#             return
#         msg = msg[msg.find(' '):]
#         users_to_check = msg.split(' ')
#         for user in users_to_check:
#             for data in :
#                 if re.search()
#
