from Configs.enum import ServerConfig
from CrawlerLib.server import create_server, get_master_option
from CrawlerLib.show_notify import show_warning, show_notify, show_debug
from CrawlerLib.socketjson import _recev, _send
from Facade.ServerProcess.ServerProcess import ServerProcess


class ServerSocket:
    def __init__(self):
        self.server = create_server(ServerConfig.IP_ADDRESS.value, ServerConfig.PORT.value, ServerConfig.NUM_CLIENT.value)
        self.clients = {
            "FB": [],
            "IG": [],
            "YT": []
        }
        self.serverProcess = ServerProcess.get_instance()

    def listen(self):
        while True:
            try:
                connection, client_address = self.server.accept()
                data = _recev(connection)
                result = self.serverProcess.process_sub(client_address, connection, self.clients, data)
                if result == -1:
                    _send(connection, {"action": "notify", "type": "fail", "ref": "undefined"})
            except BrokenPipeError:
                pass
            except Exception as e:
                show_warning('ERROR')
                print(format(e))
