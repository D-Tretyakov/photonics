import sqlite3



def format_func (inquiry, type_of_inquiry, parameters):

    if type_of_inquiry == 'добавить':
        if inquiry == "homework":
            return "INSERT INTO {} VALUES(?, ?, ?, ?, ?)".format(inquiry)
        else:#Задел на библиотеку и лекционку
            pass    
    elif type_of_inquiry == 'удалить':
        if inquiry == 'homework'
            marker = 'to_date'
            return "DELETE FROM {} WHERE {} = ?".format(inquiry, marker ) 
        else:
            pass
    elif type_of_inquiry == 'показать':
        if inquiry == 'homework':
            if parameters['subj'] is not None:   
                return "SELECT * FROM {} WHERE {} = ? ORDER BY from_date DESC LIMIT ?".format(inquiry, 'subj')
            elif parameters["date"] is not None:
                return  "SELECT * FROM {} WHERE {} = ? ORDER BY from_date DESC LIMIT ?".format(inquiry, 'to_date')
            else:
                return 'Мало данных'
        else:
            pass 
    else:
        print("Unknown ERROR in format_func")



def sql_delete (database, parameters):

    sql = database.cursor()

    inquiry = parameters['type']
    type_of_inquiry = parameters['command']
    if inquiry == "homework":#Пока делаю исключительно для домашки
        removable_marker == parameters['date']
    else:
        pass

    sql.execute(format_func(inquiry, type_of_inquiry, parameters), (removable_marker))
    database.commit()
    sql.close()

    return None

def sql_show(database, parameters):

    sql = database.cursor()

    inquiry = parameters['type']
    type_of_inquiry = parameters['command']

    if inquiry == 'homework':
                #Если  пользователь  хочет домашку по предмету и не говорит, сколько, то автоматом выдаёт 5 последних
        if  parameters['subj'] is not None  
            sql.execute(format_func(inquiry, type_of_inquiry, parameters),
                    (subj, parameters["amount"] if parameters["amount"] is not None else 5))
            hw = sql.fetchall()
        elif parameters['date'] is not None:# Если похуй на предмет, а дал конкретную дату, то выдаст всю на эту дату 
            sql.execute(format_func(inquiry, type_of_inquiry, parameters), (parameters['date']))
            hw = sql.fetchall()
        else:
            hw = "Не хватает данных "

        database.commit()
        sql.close()    
        return hw 

    else:
        pass



    
def sql_insert(database, parameters):

    sql = database.cursor()

    inquiry = parameters['type']
    type_of_inquiry['command']
    if inquiry == "homework":#Пока делаю исключительно для домашки
        added_marker == (parameters['subj'], parameters['from_date'], parameters['to_date'],
                        parameters['task'], parameters['file'])
    else:
        pass
    sql.execute(format_func(inquiry, type_of_inquiry, parameters), added_marker)
    database.commit()
    sql.close()

    return None 

def check_ERROR(parameters):
    if 'error' not in  parameters.keys()
         return True
    else 
        print("Всё хуйня Миша, давай по-новой")
        return False



def handling_command(parameters):

    response = {}
    if check_ERROR(parameters):
        # Возвращаемый мной словарь будет включать 3 ключа
        # Пишу так, просто чтоб подчеркнуть это, польше ничего там не будет 
        response['type'] = None 
        response['answ'] = None
        response['command'] = None
    
        db = sqlite3.connect('db.sqlite3')
        sql = db.cursor()

        command = parameters['command']
        response['command'] = parameters['command']
        
        if command == 'добавить':
            #Вообще, под дз нормальный словарь, который хорват написал, но для лекция и учебников понадобится другой
            #Но сейчас все равно мне нужен ещё  type: homework 
            sql_insert(db, parameters)
            response['type'] = "homework"
            response['answ'] = "Файл добавлен"
             
        elif command == 'удалить': 
            if parameters['type'] == 'homework':
                #Если команда "удалить", говоря о дз, например, то нужен словарь вида:
                #parameters = {'subj': название-предмета, 'type':'homework', 'date': какого числа удалить }
                sql_delete (db, parameters)
                response['type'] = "homework"
                response['answ'] = "Файл удален"
            else:
                pass
            
        elif command == 'показать':
            #Показать что ? В словаре, который приходит ко мне должен быть еще один ключ, type:homework или type:library или type:lection  
            hw = sql_show(db, parameters)
            response['type'] = "homework"
            response['answ'] = hw
            
            # elif parameters['type'] == 'library':#В словаре для библиотеки, который приходит ко мне, должен быть ключ typeofbook:учебник или лабник или задачник или всё#
            #             sql.execute("SELECT * FROM library ")
            #             lib = sql.fetchall()
            #             response['type'] = "library"
            #             response['answ'] = lib

            # elif parameters['type'] == "lection":# Для лекций на показ в словаре  должен быть ключ  typelection: True или False, который даст мне понимание того, нужно ли выводить всё
            #     if parameters['typelection']:
            #         sql.execute("SELECT * FROM lection ")
            #         lect = sql.fetchall()
            #     elif parameters['typelection'] is not True:#Здесь если нужно вывести только определенные лекции с номером или по просто определенному предмету 
            #             if parameters['num'] is None:#ВАЖНО! пользователь в этом случае обязательно должен ввести как минимум семестр и предмет
            #                 sql.execute("SELECT * FROM lection WHERE subj = ? and  semestr = ?", (parameters['subj'], parameters['semestr']))  
            #                 lect = sql.fetchall()
            #             elif parameters['num'] is  not None:
            #                 sql.execute("SELECT * FROM lection WHERE subj = ? and  semestr = ? and num = ?", (parameters['subj'], parameters['semestr'],  parameters['num']))  
            #                 lect = sql.fetchall()
            #     else:
            #         print("Хуйня какая-то")

            #     response['type'] = "lecture"
            #     response['answ'] = lect


        #Хуйню с исключениями в запросах к базе пока не рассматривал 
        else:
        return "Unknown ERROR" 
                
    else:
        return parameters 
        
                    
    






db = sqlite3.connect('db.sqlite3')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS homework(
    subj TEXT,
    from_date TEXT,
    to_date TEXT,
    task TEXT,
    file TEXT,
)""")


sql.execute("""CREATE TABLE IF NOT EXISTS library(
    subj TEXT,
    typeofbook TEXT,
    semestr TEXT,
    author TEXT,
    file TEXT,
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS lection(
    subj TEXT,
    semestr TEXT
    num INTEGER
    file TEXT,
    author TEXT,
)""")

db.commit()

    


