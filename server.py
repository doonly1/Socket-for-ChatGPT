import threading
from serverclass import Server


print("欢迎使用服务端程序！")
server = Server()
i = 1
while True:
    t = threading.Thread(target=server.link_one_client)
    t.start()
    print(f'第{i}线程开启')
    i += 1
    if i >3:
        print(f'等待第{i-1}线程结束\n')
        t.join()
        print(f'第{i-1}线程结束,重启线程\n')
        i = 1
        continue

