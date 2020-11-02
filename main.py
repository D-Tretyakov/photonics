from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api

from os.path import exists
import random
import json

from parsing import parse_message


def answer(vk, user_id, text):
    vk.messages.send(user_id=user_id, message=text, random_id=0)


def add_task(subj, for_date, to_date, task_text, urls):
    if exists('test_bd.json'):
        with open('test_bd.json', 'r') as f:
            bd = json.loads(f.read())
    else:
        bd = {}

    bd.setdefault(subj,[])
    bd[subj].append((str(for_date), str(to_date), task_text[1:-1], str(urls)))

    with open('test_bd.json', 'w') as f:
        f.write(json.dumps(bd, indent=4))

def show_task(subj, amount=5):
    if not exists('test_bd.json'):
        return

    with open('test_bd.json', 'r') as f:
        bd = json.loads(f.read())

    return bd[subj][:amount]


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

            result = parse_message(text)
            if result is None: # либо пришла не команда, либо еще что-то,
               continue        # что надо игнорировать

            if 'error' in result:
                answer(vk, user_id, result['error'])
                continue

            print(result)
            cmd = result['command']
            if cmd == 'добавить':
                add_task(subj=result['subj'], 
                         for_date=result['for_date'], 
                         to_date=result['to_date'], 
                         task_text=result['task_text'],
                         urls=result['urls'])
                answer(vk, user_id, 'Добавлено!')
            elif cmd == 'удалить':
                # db.delete()
                pass
            elif cmd == 'показать':
                # subj_name = res['subj']
                # tasks = db.get(subj_name)
                # answ = deins_func(tasks)
                # answer(answ)
                tasks = show_task(result['subj'], result['amount'])
                if tasks is None:
                    answer(vk, user_id, 'какое-то говно')
                else:
                    answer(vk, user_id, str(tasks))
            

if __name__ == "__main__":
    main()