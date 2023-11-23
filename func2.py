import requests
import uuid
import json

import jx
import ftoken


class PandoraAPI:
    def __init__(self, base_url, access_token=None):
        """
        Pandora HTTP API wrapper.

        Args:
        - base_url (str): Base URL of the Pandora API.
        - access_token (str, optional): Access token for authentication.
        """
        self.base_url = base_url
        # self.headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}
        self.headers = {
            'cookie':'_Secure-next-auth.apps-origin=https://121.37.20.242:18886; _Secure-next-auth.session-id=zpXdP0H8LJsrrAN4AVFQCKyXwqrHiDoG38mz9cNBqVY; session_password=qweasd333; _Secure-next-auth.session-data=MTcwMDQ5MTI1NHxOd3dBTkZGUFNsQkJUa2xRUzAwMVVVZFhRMFUzVkZKR1RUVlZXRmRHVEVwRFUxbFJOMFJJUkVKU1NGUlRTRFJYVVZNMVZGZEVTVUU9fDkSBZ1w8j_dY6uGyfe3O6eXl-j5j0MJmM3W7dFQMVqm; _puid=user-5Ifa6QGwpVSpKJu1UYQgWYAu:1700491254-UOqQf5Be0ItGMOUDHufvzZae4ZDDMSENk8yaTBny5hk%3D',
            'X-Authorization': 'Bearer 1a9EiQIZjrij7FYZMEXu6ZECMllGOG-yjJ7iL3fyyMQ'

                        }
        # self.headers = {}

    def list_models(self):
        """
        列出账号可用的模型。

        Returns:
        - dict: 模型列表的JSON响应。
        """
        url = f"{self.base_url}/backend-api/models"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def list_conversations(self, offset=1, limit=20):
        """
        以分页方式列出会话列表。

        Args:
        - offset (int, optional): 分页偏移量，默认为1。
        - limit (int, optional): 每页显示数量，默认为20。

        Returns:
        - dict: 会话列表的JSON响应。
        """
        url = f"{self.base_url}/backend-api/conversations"
        params = {'offset': offset, 'limit': limit}
        response = requests.get(url, params=params, headers=self.headers)
        return response.json()

    def delete_all_conversations(self):
        """
        删除所有会话。

        Returns:
        - str: 删除操作的结果消息。
        """
        url = f"{self.base_url}/backend-api/conversations"
        response = requests.delete(url, headers=self.headers)
        return response.text

    def get_conversation_details(self, conversation_id):
        """
        通过会话ID获取指定会话详情。

        Args:
        - conversation_id (str): 要获取详情的会话ID。

        Returns:
        - dict: 会话详情的JSON响应。
        """
        url = f"{self.base_url}/backend-api/conversation/{conversation_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def delete_conversation(self, conversation_id):
        """
        通过会话ID删除指定会话。

        Args:
        - conversation_id (str): 要删除的会话ID。

        Returns:
        - str: 删除操作的结果消息。
        """
        url = f"{self.base_url}/backend-api/conversation/{conversation_id}"
        response = requests.delete(url, headers=self.headers)
        return response.text

    def set_conversation_title(self, conversation_id, new_title):
        """
        通过会话ID设置指定的会话标题。

        Args:
        - conversation_id (str): 要设置标题的会话ID。
        - new_title (str): 新的会话标题。

        Returns:
        - str: 设置操作的结果消息。
        """
        url = f"{self.base_url}/backend-api/conversation/{conversation_id}"
        data = {'title': new_title}
        response = requests.patch(url, json=data, headers=self.headers)
        return response.text

    def generate_conversation_title(self, conversation_id, model, message_id):
        """
        自动生成指定新会话的标题，通常首次问答后调用。

        Args:
        - conversation_id (str): 要生成标题的会话ID。
        - model (str): 对话所使用的模型。
        - message_id (str): ChatGPT回复的那条消息的ID。

        Returns:
        - str: 生成的新标题。
        """
        url = f"{self.base_url}/backend-api/conversation/gen_title/{conversation_id}"
        data = {'message_id': message_id}
        response = requests.post(url, json=data, headers=self.headers,verify=False)
        return response.text

    def talk_to_chatgpt(self, prompt, model, message_id, parent_message_id=None, conversation_id=None, stream=True):
        """
        向ChatGPT提问，等待其回复。

        Args:
        - prompt (str): 提问的内容。
        - model (str): 对话使用的模型，通常整个会话中保持不变。
        - message_id (str): 消息ID，通常使用str(uuid.uuid4())来生成一个。
        - parent_message_id (str, optional): 父消息ID，首次同样需要生成。之后获取上一条回复的消息ID即可。
        - conversation_id (str, optional): 首次对话可不传。ChatGPT回复时可获取。
        - stream (bool, optional): 是否使用流的方式输出内容，默认为True。

        Returns:
        - dict: ChatGPT的回复。
        """
        url = f"{self.base_url}/backend-api/conversation"

        # {"action":"next","messages":[{"id":"aaa26f7a-0e5b-4f8f-b8dd-8404a2671c25","author":{"role":"user"},"content":{"content_type":"text","parts":["来个笑话"]},"metadata":{}}],"parent_message_id":"aaa1dfa6-38cc-4222-b46a-16b1a3676e71","model":"gpt-4","timezone_offset_min":-480,"suggestions":["Tell me a random fun fact about the Roman Empire","Make up a 5-sentence story about \"Sharky\", a tooth-brushing shark superhero. Make each sentence a bullet point.","I have a photoshoot tomorrow. Can you recommend me some colors and outfit options that will look good on camera?","Come up with 5 concepts for a retro-style arcade game."],"history_and_training_disabled":false,"arkose_token":"48817995ee33abfe9.5988076704|r=ap-southeast-1|meta=3|metabgclr=transparent|metaiconclr=%23757575|guitextcolor=%23000000|pk=35536E1E-65B4-4D96-9D97-6ADB7EFF8147|at=40|sup=1|rid=5|ag=101|cdn_url=https%3A%2F%2Fclient-api.arkoselabs.com%2Fcdn%2Ffc|lurl=https%3A%2F%2Faudio-ap-southeast-1.arkoselabs.com|surl=https%3A%2F%2Fclient-api.arkoselabs.com|smurl=https%3A%2F%2Fclient-api.arkoselabs.com%2Fcdn%2Ffc%2Fassets%2Fstyle-manager","conversation_mode":{"kind":"primary_assistant"},"force_paragen":false,"force_rate_limit":false}
        _token = ftoken.rttoken()
        print("_token",_token)
        data = {
            "action": "next",
            "messages": [
                {
                    "id": message_id,
                    "author": {"role": "user"},
                    "content": {"content_type": "text", "parts": [prompt]},
                    "metadata": {}
                }
            ],
            "parent_message_id": parent_message_id,
            "model": model,
            "timezone_offset_min": -480,
            "suggestions": [
                "Tell me a random fun fact about the Roman Empire",
                 "Make up a 5-sentence story about \"Sharky\", a tooth-brushing shark superhero. Make each sentence a bullet point.",
                 "I have a photoshoot tomorrow. Can you recommend me some colors and outfit options that will look good on camera?",
                 "Come up with 5 concepts for a retro-style arcade game."
            ],
            "history_and_training_disabled": False,
            "arkose_token": _token,
            "conversation_mode": {"kind": "primary_assistant"},
            "force_paragen": False,
            "force_rate_limit": False,
        }

        if conversation_id is not None:
            data['conversation_id'] = conversation_id
        if stream is not None:
            data['stream'] = stream

        # response = requests.post(url, json=data, headers=self.headers,verify=False)
        # print(response.text)
        # return response.json()

        response = requests.post(url, json=data, stream=False,verify=False, headers=self.headers)  # 使用stream=True来以流的方式接收响应数据
        print(response.text)
        # 写到文件
        with open('data.json', 'w') as f:
            f.write(response.text)
        data = response.text
        datas = data.split("\n")
        hdjson = {}
        for v in datas:
            try:
                parsed_data = jx.parse_data(v)
                if parsed_data['message']['content']['parts'] != None:
                    hdjson = parsed_data
            except:
                pass
                print(v, "失败")
        return hdjson




    def regenerate_response(self, prompt, model, message_id, parent_message_id, conversation_id, stream=True):
        """
        让ChatGPT重新生成回复。

        Args:
        - prompt (str): 提问的内容。
        - model (str): 对话使用的模型，通常整个会话中保持不变。
        - message_id (str): 上一条用户发送消息的ID。
        - parent_message_id (str): 上一条用户发送消息的父消息ID。
        - conversation_id (str): 会话ID，在这个接口不可不传。
        - stream (bool, optional): 是否使用流的方式输出内容，默认为True。

        Returns:
        - dict: ChatGPT重新生成的回复。
        """
        url = f"{self.base_url}/backend-api/conversation/regenerate"
        data = {'prompt': prompt, 'model': model, 'message_id': message_id,
                'parent_message_id': parent_message_id, 'conversation_id': conversation_id, 'stream': stream}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def continue_conversation(self, model, parent_message_id, conversation_id, stream=True):
        """
        让ChatGPT讲之前的恢复继续下去。

        Args:
        - model (str): 对话使用的模型，通常整个会话中保持不变。
        - parent_message_id (str): 父消息ID，上一次ChatGPT应答的消息ID。
        - conversation_id (str): 会话ID。
        - stream (bool, optional): 是否使用流的方式输出内容，默认为True。

        Returns:
        - dict: ChatGPT继续会话的回复。
        """
        url = f"{self.base_url}/backend-api/conversation/goon"
        data = {'model': model, 'parent_message_id': parent_message_id,
                'conversation_id': conversation_id, 'stream': stream}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()


# Example Usage:
# Replace 'YOUR_BASE_URL' and 'YOUR_ACCESS_TOKEN' with actual values.
base_url = 'https://121.37.20.242:18886'
access_token = 'YOUR_ACCESS_TOKEN'
pandora_api = PandoraAPI(base_url, access_token)


class 问答机器人:
    def __init__(self):
        self.pandora_api = pandora_api
        self.conversation_id = None
        self.parent_message_id = None
        self.message_id = None
        # self.model = 'text-davinci-002-render-sha'
        self.model = 'gpt-4'

    def 提问(self, 文本):
        self.message_id = str(uuid.uuid4())
        if self.conversation_id is None:
            self.parent_message_id = str(uuid.uuid4())
            response = pandora_api.talk_to_chatgpt(文本, self.model, self.message_id,
                                                   parent_message_id=self.parent_message_id, stream=False)
            try:
                pandora_api.generate_conversation_title(response['conversation_id'], self.model, response['message']['id'])
            except:
                pass
                return response['message']['content']['parts'][0]

        else:
            response = pandora_api.talk_to_chatgpt(文本, self.model, self.message_id,
                                                   parent_message_id=self.parent_message_id,
                                                   conversation_id=self.conversation_id, stream=False)
        # logging.info(response)
        print(response)
        self.parent_message_id = response['message']['id']
        self.conversation_id = response['conversation_id']

        return response['message']['content']['parts'][0]
        return response


if __name__ == '__main__':
    问答机器人 = 问答机器人()
    print(问答机器人.提问('你好'))
    print(问答机器人.提问('你会js吗'))
    print(问答机器人.提问('写一个hello world程序'))

    # Use the methods as needed, for example:
    # models = pandora_api.list_models()
    # print("Available Models:", models)
    #
    # conversations = pandora_api.list_conversations()
    # print("Conversations:", conversations)
    # Example of calling the talk_to_chatgpt method:
    # prompt = '你会python吗'
    # model = 'text-davinci-002-render-sha'  # Replace with the actual model you want to use
    # message_id = str(uuid.uuid4())  # Generate a unique message ID
    # parent_message_id = str(uuid.uuid4())  # Generate a unique message ID
    # print("message_id", message_id)
    # print("parent_message_id", parent_message_id)
    # # {"prompt":"你好","message_id":"1f18889e-79c9-4af1-beb2-a2f008d220d2","parent_message_id":"40ee7d15-aebd-40e3-a602-a029d8c4c302","model":"text-davinci-002-render-sha","timezone_offset_min":-480}
    # response = pandora_api.talk_to_chatgpt(prompt, model, message_id, parent_message_id=parent_message_id, stream=False)
    # #  {
    # #   "conversation_id": "93946d8f-fcf8-478d-a400-19339cb6f7a8",
    # #   "error": null,
    # #   "message": {
    # #     "author": {
    # #       "metadata": {},
    # #       "name": null,
    # #       "role": "assistant"
    # #     },
    # #     "content": {
    # #       "content_type": "text",
    # #       "parts": [
    # #         "print(\"Hello, world!\")"
    # #       ]
    # #     },
    # #     "create_time": 1697671925.506507,
    # #     "end_turn": true,
    # #     "id": "b9129068-20fe-4d36-a5fa-30dd5f4acea2",
    # #     "metadata": {
    # #       "finish_details": {
    # #         "stop_tokens": [
    # #           100260
    # #         ],
    # #         "type": "stop"
    # #       },
    # #       "is_complete": true,
    # #       "message_type": "next",
    # #       "model_slug": "text-davinci-002-render-sha",
    # #       "parent_id": "9f34ee2f-5243-4a89-ad50-9f13bb62553b",
    # #       "timestamp_": "absolute"
    # #     },
    # #     "recipient": "all",
    # #     "status": "finished_successfully",
    # #     "update_time": null,
    # #     "weight": 1.0
    # #   }
    # # }
    # print("ChatGPT's Reply:", response)
    # print("conversation_id", response['conversation_id'])
    # print("parts", response['message']['content']['parts'])
    #
    # prompt = '写一个hello world程序'
    # parent_message_id = response['message']['id']
    # conversation_id = response['conversation_id']
    # message_id = str(uuid.uuid4())  # Generate a unique message ID
    #
    # response = pandora_api.talk_to_chatgpt(prompt, model, message_id,
    #                                        parent_message_id=parent_message_id,
    #                                        conversation_id=conversation_id, stream=False)
    #
    # print("ChatGPT's Reply:", response)
    # print("conversation_id", response['conversation_id'])
    # print("parts", response['message']['content']['parts'])
