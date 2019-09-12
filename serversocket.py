from CrawlerLib.helper import print_header_log
from Server.ServerSocket import ServerSocket


print_header_log()
s = ServerSocket()
s.listen()
