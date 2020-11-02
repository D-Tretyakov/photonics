
"""
Функция на вход запрашивает список со всеми домашками по конкретному предмету.
На выходе выдает строку -- готовый ответ пользователю.
"""
def ans_func(tasks):
    answer = "ЗАДАНИЯ ПО ПРЕДМЕТУ:"+"\n"
    for task in tasks:
        answer += "Домашка " + str(tasks.index(task)) + ":\t" + task + "\n"
    return answer
