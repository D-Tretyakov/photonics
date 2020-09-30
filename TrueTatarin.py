def parsing(str1 ,id , name): #  Предполагаю что запрос будет в виде: !Добавить(Удалить, показать) дз по ....... за ....... дедлайн .......
    dict1 = {}
    list1 = str1.split()  # разделю запрос на слова
    if list1[0] == '!Добавить':  # Реализация Python Switch Case с помощью if-elif
        dict1['subj'] = list1[3]
        dict1['from_date'] = list1[5]
        dict1['to_date'] = list1[7]
        dict1['files'] =  ' '.join([list1[i] for i in range(8, len(list1))])

    elif list1[0] == '!Показать':
        dict1['subj'] = list1[3]
        dict1['to_date'] = list1[5]   # Если просится найти дз на завтра , то ожидаю шаблон :!Показать дз по ..... на ....
        dict1['amount'] = ' Здесь должна быть ,видимо, ссылка на библиотеку в вк '    # Тут выводится нужная домашка на завтра ,к примеру

    elif list1[0] == '!Удалить':
        dict1['subj'] = list1[3]
        dict1['task_number'] = list1[5]    # Ожидаю шаблон : !Удалить дз по .... за .....(число)

    else:
        return print("Пошел нахуй")

    dict2 = {'id': id, 'name': name}   # Я предположил , что в функцию также могут предоваться значения id, name, если нет , что тут значения по умолчанию
    list1.pop(0)
    str2 = ' '.join(list1)
    dictfull = {'command': str2 , 'parameters': dict1, 'user': dict2}
    return print(dictfull)

str= input()
parsing(str ,2323, 'Rus')







