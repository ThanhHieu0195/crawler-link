from Configs.enum import ServerConfig
from CrawlerLib.server import create_server
from CrawlerLib.show_notify import show_warning
from CrawlerLib.socketjson import _recev, _send
from Facade.ServerProcess.ServerProcess import ServerProcess
import threading


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
            connection, client_address = self.server.accept()
            try:
                x = threading.Thread(target=self.subscribe, args=(connection, client_address), daemon=True)
                x.start()
            except BrokenPipeError:
                pass
            except Exception as e:
                print('code1122')
                show_warning('ERROR')
                print(format(e))

    def subscribe(self, connection, client_address):
        data = _recev(connection)
        self.serverProcess.process_sub(client_address, connection, self.clients, data)
