import datetime
import re


def convert_date(str_date):
    # дата должна приходить в формате дд.мм.гггг (10.11.2020)
    result = re.search(r'\d{2}.\d{2}.\d{4}', str_date)
    if result is not None:
        return datetime.datetime.strptime(str_date, '%d.%m.%Y')
    else:
        return 'None'


def convert_urls(urls_str):
    pattern = r'\bhttps://\S+\b'  # url каждого файла должен идти через пробелы
    result = re.findall(pattern, urls_str)
    if result is not None:
        return result
    else:
        return 'None'


def parse_message(message):
    if not message.startswith('!'):  # проверка, комнда ли пришла
        return {'error': 'invalid command format'}

    if message.startswith('!показать'):
        if 'на' in message:
            pattern = r'!показать\sдз\sпо\s(\D*)\sна\s(\S*)'  # шаблон для команды
            result = re.search(pattern, message)  # возвращаем список из
            if not result:
                return {'error': 'invalid command format'}
            args = result.groups()
            subj = args[0]
            to_date = args[1]
            return {'command': 'показать', 'subj': subj, 'to_date': to_date, 'amount': '1'}

        else:
            pattern = r'!показать\sдз\sпо\s(\D*)'
            result = re.search(pattern, message)  # возвращаем список из
            if not result:
                return {'error': 'invalid command format'}
            args = result.groups()
            subj = args[0]
            return {'command': 'показать', 'subj': subj, 'amount': '5'}



    elif message.startswith('!добавить'):
        # !добавить дз по subj на from_date до to_date "task_text" [url1 url2 url3] <- структура команды
        pattern = r'!добавить\sдз\sпо\s(\D*)\sна\s(\S*)\sдо\s(\S*)\s(\"(.*?)\")\s(\[(.*?)\])'
        result = re.search(pattern, message)

        if not result:
            return {'error': 'invalid command format'}

        args = result.groups()
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
        pattern = r'!удалить\sдз\sпо\s(\D*)\sза\s(\S*)'  # TODO дописать
        result = re.search(pattern, message)
        if not result:
            return {'error': 'invalid command format'}
        args = result.groups()
        subj = args[0]
        for_date = args[1]
        return {'command': 'удалить', 'subj': subj, 'for_date': for_date}


str1 = str(input())
print(parse_message(str1))