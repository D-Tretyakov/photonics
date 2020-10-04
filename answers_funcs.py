
def ans_func(tasks):
    answer = "ЗАДАНИЯ ПО ПРЕДМЕТУ:\n"
    for task in tasks:
        answer += "Домашка " + tasks.index(task) + ":\t" + task + "\n"
    return answer
