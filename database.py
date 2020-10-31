import sqlite3
import datetime as dt


def format_func (inquiry, type_of_inquiry, parameters):

    if type_of_inquiry == 'добавить':
        if inquiry == "homework":
            return "INSERT INTO {} VALUES(?, ?, ?, ?, ?)".format(inquiry) 
        #if здесь, потому что потом будут и для inquiry == "library" и "lectures"  *****
    elif type_of_inquiry == 'удалить':
        if inquiry == 'homework':
            return "DELETE FROM homework WHERE subj = ? AND from_date = ?" 
        #аналогично *****
    elif type_of_inquiry == 'показать':
        if inquiry == 'homework':
            if parameters['subj'] is not None:   
                return "SELECT * FROM {} WHERE {} = ? ORDER BY to_date DESC LIMIT ?".format(inquiry, 'subj')
            elif parameters["to_date"] is not None:
                return  "SELECT * FROM {} WHERE {} = ? ".format(inquiry, 'to_date')
        #аналогично *****


def sql_insert(database, parameters):

    sql = database.cursor()

    inquiry = parameters['type']
    type_of_inquiry = parameters['command']
    if inquiry == "homework":#Пока делаю исключительно для домашки
        added_marker = (parameters['subj'], parameters['from_date'].date().strftime("%Y-%m-%d"), parameters['to_date'].date().strftime("%Y-%m-%d"),
                        parameters['task'], parameters['file'])
    
    sql.execute(format_func(inquiry, type_of_inquiry, parameters), added_marker)
    database.commit()
    sql.close()

    return None

def sql_delete (database, parameters):

    sql = database.cursor()

    inquiry = parameters['type']
    type_of_inquiry = parameters['command']

    if inquiry == "homework":
        #Пока делаю исключительно для домашки
        removable_marker1 = parameters['subj']
        removable_marker2 = parameters['from_date']
    # #аналогично *****
    print(parameters)
    sql.execute(format_func(inquiry, type_of_inquiry, parameters), (removable_marker1, parameters['from_date'].date().strftime("%Y-%m-%d")))
    database.commit()
    sql.close()

    return None

def sql_show(database, parameters):

    sql = database.cursor()

    inquiry = parameters['type']
    type_of_inquiry = parameters['command']
    if inquiry == 'homework':
        print(parameters)
        #Если  пользователь  хочет домашку по предмету и не говорит, сколько, то автоматом выдаёт 5 последних
        if  parameters['subj'] is not None: 
            sql.execute(format_func(inquiry, type_of_inquiry, parameters),
                        (parameters['subj'], parameters["amount"] if parameters["amount"] is not None else 5))
            hw = sql.fetchall()
        elif parameters['to_date'] is not None:# Если похуй на предмет, а дал конкретную дату, то выдаст всю на эту дату 
            sql.execute(format_func(inquiry, type_of_inquiry, parameters), (parameters['to_date'].date().strftime("%Y-%m-%d"),))
            hw = sql.fetchall()
        #аналогично *****
        database.commit()
        sql.close()    
        return hw

#Нужна, чтобы реверсить дату, например 281020 -> 201028. Для чего нужно ? 
#В базе хранится именно так и связано с сортировкой SQL
# А так мне стыдно за это говно 
def date_func(parameters):
    if type(parameters) == dict:    
        for key in parameters.keys():
            if key == 'to_date':
                parameters['to_date'] = dt.datetime.strptime(parameters['to_date'], "%d%m%Y") 
            if key == 'from_date':
                parameters['from_date'] = dt.datetime.strptime(parameters['from_date'], "%d%m%Y")
        return parameters 
    else: 
        #Используется лишь в редактировании при показе домашки 
        hw = list()
        for old_elements in parameters:
            new_elements = list(old_elements)
            new_elements[1] = dt.datetime.strptime(old_elements[1], "%Y-%m-%d")
            new_elements[2] = dt.datetime.strptime(old_elements[2], "%Y-%m-%d")
            hw.append(new_elements) 
        return hw



def check_ERROR(parameters):
    if 'error' not in  parameters.keys():
        return True
    else: 
        return False



def handling_command(parameters):

    response = {}
    if check_ERROR(parameters):
        # Возвращаемый мной словарь будет включать 3 ключа
        # Пишу так, просто чтоб подчеркнуть это, больше ничего там не будет 
        db = sqlite3.connect('db1.sqlite3')
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS homework(
            subj TEXT,
            from_date TEXT,
            to_date TEXT,
            task TEXT,
            file TEXT
        )""")


        sql.execute("""CREATE TABLE IF NOT EXISTS library(
            subj TEXT,
            typeofbook TEXT,
            semestr TEXT,
            author TEXT,
            file TEXT
        )""")

        sql.execute("""CREATE TABLE IF NOT EXISTS lection(
            subj TEXT,
            semestr TEXT
            num INTEGER
            file TEXT,
            author TEXT
        )""")

        db.commit()

        response['type'] = None 
        response['answ'] = None
        response['command'] = None
    
        

        for i in sql.execute("SELECT * FROM homework"):
           print(i)  

        command = parameters['command']
        response['command'] = parameters['command']
        parameters = date_func(parameters)

        if command == 'добавить':
            #Вообще, под дз нормальный словарь, который хорват написал, но для лекция и учебников понадобится другой
            #Но сейчас все равно мне нужен ещё  type: homework 
            if parameters['type'] == 'homework':
                sql_insert(db, parameters)
                response['type'] = "homework"
                response['answ'] = "Файл добавлен"
            #аналогично *****
        elif command == 'удалить': 
            if parameters['type'] == 'homework':
                #Если команда "удалить", говоря о дз, например, то нужен словарь вида:
                #parameters = {'subj': название-предмета, 'type':'homework', 'date': какого числа удалить }
                sql_delete (db, parameters)
                response['type'] = "homework"
                response['answ'] = "Файл удален"
            #аналогично *****
            
        elif command == 'показать':
            #Показать что ? В словаре, который приходит ко мне должен быть еще один ключ, type:homework или type:library или type:lection  
            hw = sql_show(db, parameters)
            response['type'] = "homework"
            hw = date_func(hw)
            response['answ'] = hw
        
        else:
            db.commit()
            sql.close()
            response['error'] = 'Не нашел команду'
            return  response
        print('---------------------------------------------------------------------------------------------')
        for i in sql.execute("SELECT * FROM homework"):
            print(i)  
        db.commit()
        sql.close()   

        return response
                
    else:
        response['error'] = 'Сработал Сheck Error'
        return response 
        
                    

        
# Потестил, все работает

par2 = {'subj': 'Тополя', 'type':'homework', 'from_date':'31022020', 'command':'удалить'}   
par1 = {'type':'homework', 'command':'добавить', 'subj':'Кванты', 'from_date':'23022020', 'to_date':'07122020', 'task':'нихуя', 'file':None}  
par3 = {'type':"homework", 'command':'показать', 'subj': "Атомка", 'to_date': None, 'amount':2  }
par4 = {'type':"homework", 'command':'показать', 'subj': None, 'to_date': '07122020', 'amount':None }   
par5 = {'error': "Хуйня какая-то"}
a = handling_command(par4)
print(a)
