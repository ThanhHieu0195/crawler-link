from Server.ServerSocket import ServerSocket
import time


print("=========================================")
print("Today: " + time.strftime('%d-%m-%Y %H:%M'))
s = ServerSocket()
s.listen()
