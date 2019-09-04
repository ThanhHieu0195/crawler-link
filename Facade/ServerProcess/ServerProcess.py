from Facade.ServerProcess.Subs.AssignProcess import AssignProcess
from Facade.ServerProcess.Subs.SubscribeProcess import SubscribeProcess


class ServerProcess:
    Main=None

    def __init__(self ):
        self.subs = {
            AssignProcess.get_name(): AssignProcess(),
            SubscribeProcess.get_name(): SubscribeProcess()
        }

    @staticmethod
    def get_instance():
        if ServerProcess.Main is None:
            ServerProcess.Main= ServerProcess()
        return ServerProcess.Main

    # define response
    def process_sub(self, client_address, connection, clients, data):
        self.client_address = client_address
        self.connection = connection
        self.clients = clients

        if 'action' in data and data['action'] in self.subs:
            return self.subs[data['action']].process_sub(self, data)
        return -1
