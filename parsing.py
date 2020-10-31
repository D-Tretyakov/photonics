import datetime
import re


def convert_date(str_date):
    # дата должна приходить в формате дд.мм.гггг (10.11.2020)
    result = re.search(r'\d{2}.\d{2}.\d{4}', str_date)
    if result is not None:
        return datetime.datetime.strptime(str_date, '%d.%m.%Y')
    else:
        return None


def convert_urls(urls_str):
    # TODO надо дописать (надо еще валидировать каждый url)
    return []


def parse_message(message):
    if not message.startswith('!'): # проверка, комнда ли пришла
        return

    if message.startswith('!показать'):
        pattern = r'!показать\s(\w*)\sна\s(\S*)\s(\d*)' # шаблон для команды
        args = re.search(pattern, message).groups() # возвращаем список из 
                                                    # аргументов команды

        if not args:
            return {'error': 'invalid command format'}

        subj = args[0] 
        for_date_str = args[1]
        amount = args[2]

        for_date = convert_date(for_date_str)
        if for_date is None: 
            return {'error': 'invalid date'}
        
        return {'command': 'показать', 'subj': subj, 'for_date': for_date, 'amount': amount}

    elif message.startswith('!добавить'):
        # !добавить subj на from_date до to_date "task_text" [url1 url2 url3] <- структура команды
        pattern = r'!добавить\s(\w*)\sна\s(\S*)\sдо\s(\S*)\s(\"(.*?)\")\s(\[(.*?)\])'
        args = re.search(pattern, message).groups()

        if not args:
            return {'error': 'invalid command format'}
        
        subj = args[0] 
        for_date_str = args[1]
        to_date_str = args[2]
        task_text = args[3]
        urls_str = args[4]

        for_date = convert_date(for_date_str)
        to_date = convert_date(to_date_str)
        if for_date is None or to_date is None:
            return {'error': 'invalid date'}
        
        urls = convert_urls(urls_str)

        return {'command': 'добавить',
                'subj': subj, 
                'for_date': for_date, 
                'to_date': to_date, 
                'task_text': task_text,
                'urls': urls}

    elif message.startswith('!удалить'):
        # TODO дописать
        return None     