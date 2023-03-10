import threading

from serverclass import Server

print("欢迎使用服务端程序！")

server = Server()
# 这里使用多线程可以避免服务器阻塞在一个客户端上
server.link_one_client()
