from Client.ClientSocket import ClientSocket
from CrawlerLib.helper import print_header_log

print_header_log()
while True:
    client = ClientSocket()
    client.listen()
