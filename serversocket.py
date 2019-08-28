from Server.ServerSocket import ServerSocket
import time


print("=========================================")
print("Today: " + time.strftime('%d-%m-%Y %H:%M', time.gmtime()))
s = ServerSocket()
s.listen()
