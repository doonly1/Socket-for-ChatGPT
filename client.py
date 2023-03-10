from clientclass import Client



print("欢迎使用客户端程序！")
with open("api_key.txt","r",encoding="utf-8") as f:
    api_key = f.read()
with open("ip.txt","r",encoding="utf-8") as f:
    ip = f.read()


client = Client()
client.link_server(addr=(ip,8080),api_key=api_key)
