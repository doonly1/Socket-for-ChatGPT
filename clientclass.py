import socket
import rsa
import pickle
from cryptography.fernet import Fernet
import hashlib
from errorclass import AuthenticationError

class Client:

    def __init__(self):
        # 产生非对称密钥
        self.asyKey = rsa.newkeys(2048)
        # 公钥和私钥
        self.publicKey = self.asyKey[0]
        self.privateKey = self.asyKey[1]


    def link_server(self, addr=('localhost', 8080), api_key=""):
        # 创建socket通信对象
        # 默认使用AF_INET协议族，即ipv4地址和端口号的组合以及tcp协议
        clientSocket = socket.socket()
        # 默认连接服务器地址为本机ip和8080端口
        clientSocket.connect(addr)

        # 向服务器传递公钥，和该公钥字符串化后的sha256值
        print("正在向服务器传送公钥")
        sendKey = pickle.dumps(self.publicKey)
        sendKeySha256 = hashlib.sha256(sendKey).hexdigest()
        clientSocket.send(pickle.dumps((sendKey, sendKeySha256)))

        # 接受服务器传递的密钥并进行解密
        symKey, symKeySha256 = pickle.loads(clientSocket.recv(1024))
        if hashlib.sha256(symKey).hexdigest() != symKeySha256:
            raise AuthenticationError("密钥被篡改！")
        else:
            self.symKey = pickle.loads(rsa.decrypt(symKey, self.privateKey))
            print("密钥交换完成")

        # 初始化加密对象
        f = Fernet(self.symKey)

        en_api_key = f.encrypt(api_key.encode())
        clientSocket.send(en_api_key)
        en_recvData = clientSocket.recv(1024)
        recvData = f.decrypt(en_recvData).decode()
        print(recvData)
        

        while True:

            sendData = input("你：")
            en_sendData = f.encrypt(sendData.encode())
            clientSocket.sendall(en_sendData)

            # 接收服务端的加密消息
            total_data = bytes()
            while True: 
                en_recvData = clientSocket.recv(1024)
                total_data += en_recvData
                if len(en_recvData) < 1024:
                    break
            recvData = f.decrypt(total_data).decode()
            print(f"GPT：{recvData}")


