import re

def parsing(str1 ,id , name):
    dict1 = {}
    if str1[0] != '!':
        return  {'error': 'пиши по шаблону'}
    list1 = str1.lower().split()                    # разделю запрос на слова

                             # для чтения ссылок

    if list1[0] == '!добавить':                 # Реализация Python Switch Case с помощью if-elif

        list2 = ['!добавить', 'дз', 'по', 'за', 'дедлайн']
        f = 0
        for i in list2:                     # Здесь провереяю корректность запроса (наличие нужных слов , в нужной последовательности)
            if i in list1 and list1.index(i) >= f:
                f = list1.index(i)
                continue
            else:
                return  {'error': 'пиши по шаблону'}

        if list1.index('за') != 4:                  #  На тот случай , если предмет будет из двух и более  строчек - объединяю  элементыц списка
            list1[3:list1.index('за')] = [' '.join(list1[3 :list1.index('за')])]

        if list1.index('дедлайн') != 6:
            list1[5:list1.index('дедлайн')] = [' '.join(list1[5:list1.index('дедлайн')])]


        dict1['type'] = 'homework'             #  Предполагаю что запрос будет в виде: !Добавить(Удалить, показать) дз по ....... за ....... дедлайн .......
        dict1['command'] = 'добавить'
        dict1['subj'] = list1[3]
        dict1['from_date'] = list1[5]
        dict1['to_date'] = list1[list1.index('дедлайн')+1]

        if re.search("(?P<url>https?://[^\s]+)", str1):                #  по ключу 'file'  передаю ссылку ( Пока только для одного файла , после сделаю для нескольких )
            dict1['task'] =  ' '.join([list1[i] for i in range(8, len(list1)-1)])
            dict1['file'] = list1[len(list1)-1]
        else:
            dict1['task'] = ' '.join([list1[i] for i in range(8, len(list1))])
            dict1['file'] = 'None'


    elif list1[0] == '!показать':
        dict1['type'] = 'homework'
        dict1['command'] = 'показать'
        if 'на' in list1:                   # Разветление команды показать
            list2 = ['!показать', 'дз', 'по' ,'на']
            f=0
            for i in list2:                # Здесь также провереяю корректность запроса (наличие нужных слов , в нужной последовательности)
                if i in list1 and list1.index(i) >= f:
                    f = list1.index(i)
                    continue
                else:
                    return  {'error': 'пиши по шаблону'}

            if list1.index('на') != 4:             # На тот случай , если предмет будет из двух и более строчек - объединяю два элемента списка
                list1[3 : list1.index('на')] = [' '.join(list1[3 : list1.index('на')])]
            dict1['subj'] = list1[3]
            dict1['to_date'] =  ' '.join(list1[5:len(list1)])     # Если просится найти дз на завтра или на какое-то число , то ожидаю шаблон :!Показать дз по ..... на ....
            dict1['amount'] = '1'         # Если дз на какое-то число , то количество 1 ставлю

        else:
            list2 = ['!показать', 'дз', 'по']
            f = 0
            for i in list2:                                          # Здесь также провереяю корректность запроса (наличие нужных слов , в нужной последовательности)
                if i in list1 and list1.index(i) >= f:
                    f = list1.index(i)
                    continue
                else:
                    return  {'error': 'пиши по шаблону'}

            dict1['subj'] = ' '.join(list1[3:len(list1)])
            dict1['to_date'] = 'None'
            dict1['amount'] = 'None'     # Здесь ты, Тимур,уже выводишь последние 5 домашек по предмету


    elif list1[0] == '!удалить':
        list2 = ['!удалить', 'дз', 'по', 'за']
        f = 0
        for i in list2:                  # Здесь также провереяю корректность запроса (наличие нужных слов , в нужной последовательности)
            if i in list1 and list1.index(i) >= f:
                f = list1.index(i)
                continue
            else:
                return  {'error': 'пиши по шаблону'}
        dict1['type'] = 'homework'
        dict1['command'] = 'удалить'

        if list1.index('за') != 4:  # На тот случай , если предмет будет из двух  и более строчек - объединяю два элемента списка
            list1[3:list1.index('за')] = [' '.join(list1[3:list1.index('за')])]
        dict1['subj'] = list1[3]
        dict1['from_date'] = ' '.join(list1[5:len(list1)])    # Ожидаю шаблон : !Удалить дз по .... за .....(число)

    else:
        return  {'error': 'пиши по шаблону'}

    dict2 = {'id': id, 'name': name}   # Я предположил , что в функцию также могут предоваться значения id, name, если нет , что тут значения по умолчанию

    dictfull = { 'parameters': dict1, 'user': dict2}

    return dictfull

str1 = str(input())
print(parsing(str1, '232323', 'авава'))










