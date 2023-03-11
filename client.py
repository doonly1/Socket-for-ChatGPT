from clientclass import Client



print("欢迎使用客户端程序！")

with open("config.txt","r",encoding="utf-8") as f:
    lines = f.read().splitlines()
    key = lines[0].split('=')[1]
    ip  = lines[1].split('=')[1]


client = Client()
client.link_server(addr=(ip,8080),api_key=key)
