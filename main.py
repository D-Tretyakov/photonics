import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


from parsing import parse_message


def main():
    """ 
    Пример использования bots longpoll
    https://vk.com/dev/bots_longpoll
    """

    vk_session = vk_api.VkApi(token='a9348fbc4a04e6ba9e6082f09bfbf310d8e67e220601a374dff5d3faff58db8b8cecf6d59b0c6c8acab40')
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, '175910367')

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            # print(event.obj.__dict__)
            # {'date': 1596138570, 'from_id': 212285182, 'id': 997, 'out': 0, 'peer_id': 212285182, 'text': 'dfg', 'conversation_message_id': 65, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False}
            user_id = event.obj.message['from_id']
            text = event.obj.message['text']
            # page = vk.users.get(user_id=116584678)

            if user_id == 116584678 and random.random() > 0.3:
                vk.messages.send(user_id=user_id, message='Ты пидор', random_id=0)

            result = parse_message(text)
            if result is None: # либо пришла не команда, либо еще что-то,
               continue        # что надо игнорировать

            if 'error' in result:
                vk.messages.send(user_id=user_id, message=result['error'], random_id=0)
                continue

            print(result)
            cmd = result['command']
            if cmd == 'добавить':
                # add_task(subj=result['subj'], 
                #          for_date='for_date', 
                #          to_date=result['to_date'], 
                #          task_text=result['task_text'],
                #          urls=result['urls'])
                answer = ' '.join(str(value) for value in result.values())
                vk.messages.send(user_id=user_id, message=answer, random_id=0)
            elif cmd == 'удалить':
                # db.delete()
                pass
            elif cmd == 'показать':
                # subj_name = res['subj']
                # tasks = db.get(subj_name)
                # answ = deins_func(tasks)
                # answer(answ)
                pass
            

if __name__ == "__main__":
    main()