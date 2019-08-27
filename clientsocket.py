from Client.ClientSocket import ClientSocket
from CrawlerLib.helper import get_time_log

print("=========================================")
print("Today: " + get_time_log())
client = ClientSocket()
client.listen()
