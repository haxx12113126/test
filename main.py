import logging
import time
import threading
from flask import Flask, request
import func2

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.StreamHandler(),  # Log to console
                        logging.FileHandler('app.log')  # Log to a file
                    ])
机器人列表 = {}
# 设置 60*60*24的定时任务 清空一次机器人列表
def 清空机器人线程():
    while True:
        global 机器人列表
        机器人列表 = {}
        time.sleep(60*60*24)



@app.route('/post_chatgpt', methods=['POST'])
def receive_data():
    # 获取 post 参数 名称为 data
    messages = request.form.get('messages')
    id = request.form.get('id')
    # 变量 机器人列表 将id 作文map的key放置机器人对象
    if id not in 机器人列表:
        机器人列表[id] = func2.问答机器人()

    机器人 = 机器人列表[id]
    response = 机器人.提问(messages)

    return response

if __name__ == '__main__':


    t = threading.Thread(target=清空机器人线程)
    t.start()

    app.run(
        host="0.0.0.0",
        port=8000, debug=True)
