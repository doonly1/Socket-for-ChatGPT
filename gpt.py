import openai
import json
import os


# 获取 api
# openai.api_key = ""


class ChatGPT:
    
    def __init__(self, user):
        self.user = user
        self.messages = [{"role": "system", "content": ""}]
        self.filename="./user_messages.json"

    def ask_gpt(self):
        rsp = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=self.messages,
        )
        
        if self.messages[-1]["content"].startswith("生成图像："):
            response = openai.Image.create(
              prompt=self.messages[-1]["content"].split('：')[1],
              n=1,
              size="1024x1024"
            )
            image_url = response['data'][0]['url']
            return image_url

            
        return rsp.get("choices")[0]["message"]["content"]
    
    def writeTojson(self):
        try:
            # 判断文件是否存在，并创建
            if not os.path.exists(self.filename):
                with open(self.filename, "w") as f:
                    pass      
            # 读取         
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                msgs = json.loads(content) if len(content) > 0 else {}
            # 追加
            msgs.update({self.user : self.messages})
            # 写入
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(msgs, f)
        except Exception as e:
            print(f"错误代码：{e}")


def main():
    user = input("请输入对话名称: ")
    chat = ChatGPT(user)
    # 循环
    while 1:
        # 限制对话次数
        if len(chat.messages) >= 11:
            print("******************************")
            print("*********强制重置对话**********")
            print("******************************")
            # 写入之前信息
            chat.writeTojson()
            user = input("请输入对话名称: ")
            chat = ChatGPT(user)

        # 提问
        q = input(f"【{chat.user}】：")

        # 逻辑判断
        if q == "0":
            print("*********退出程序**********")
            # 写入之前信息
            chat.writeTojson()
            break
        elif q == "1":
            print("**************************")
            print("*********重置对话**********")
            print("**************************")
            # 写入之前信息
            chat.writeTojson()
            user = input("请输入对话名称: ")
            chat = ChatGPT(user)
            continue
            
        # 提问-回答-记录
        chat.messages.append({"role": "user", "content": q})
        answer = chat.ask_gpt()
        print(f"【ChatGPT】：{answer}")
        chat.messages.append({"role": "assistant", "content": answer})


if __name__ == '__main__':
    main()

