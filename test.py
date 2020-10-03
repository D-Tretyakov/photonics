import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

def main():
    """ Пример использования bots longpoll
        https://vk.com/dev/bots_longpoll
    """

    vk_session = vk_api.VkApi(token='a9348fbc4a04e6ba9e6082f09bfbf310d8e67e220601a374dff5d3faff58db8b8cecf6d59b0c6c8acab40')
    vk = vk_session.get_api()

    # тимур пидорас
    longpoll = VkBotLongPoll(vk_session, '175910367')

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            # print(event.obj.__dict__)
            # {'date': 1596138570, 'from_id': 212285182, 'id': 997, 'out': 0, 'peer_id': 212285182, 'text': 'dfg', 'conversation_message_id': 65, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False}
            user_id = event.obj.message['from_id']
            text = event.obj.message['text']
            # page = vk.users.get(user_id=116584678)

            if user_id == 116584678 and random.random() > 0.3:
                vk.messages.send(user_id=user_id, message='Хорват пидор', random_id=0)

            vk.messages.send(user_id=user_id, message=text.upper(), random_id=0)

if __name__ == "__main__":
    main()