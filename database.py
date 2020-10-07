import sqlite3


""" На функции до handing_command даже не смотри пока """


def format_func (inquiry, type_of_inquiry):

    if type_of_inquiry == 'добавить':
        return "INSERT INTO {} VALUES(?, ?, ?, ?, ?)".format(inquiry)     
    else:
        print("Unknown ERROR in format_func")



def sql_delete (database, date, inquiry, type_of_inquiry): 

    sql = database.cursor
    sql.execute(format_func(inquiry, type_of_inquiry), date)
    print("file was deleted")
    database.commit()
    sql.close()

    return None


    
def sql_insert(database, date, inquiry, type_of_inquiry):

    sql = database.cursor()
    sql.execute(format_func(inquiry, type_of_inquiry), date)
     print("file was added")
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
        response['type'] = None 
        response['answ'] = None
    
        db = sqlite3.connect('db.sqlite3')
        sql = db.cursor()

        command = parameters['command']
        if command == 'добавить':
            pass
        elif command == 'удалить':
            pass
        elif command == 'показать':
            #Показать что ? В словаре, который приходит ко мне должен быть еще один ключ, type:homework или type:library или type:lection  
            if parameters['type'] == 'homework':
                if parameters['subj'] is not None:#Если  пользователь  хочет домашку по предмету и не говорит, сколько, то автоматом выдаёт 5 последних   
                    sql.execute(
                        "SELECT * FROM homework WHERE subj = ? ORDER BY from_date DESC LIMIT ?",
                        (subj, parameters["amount"] if parameters["amount"] is not None else 5))
                    hw = sql.fetchall()
                elif parameters["date"] is not None:# Если похуй на предмет, а дал конкретную дату, то выдаст всю на эту дату 
                    sql.execute("SELECT * FROM homework WHERE to_date = ? ", (parameters['date']))
                    hw = sql.fetchall()
                else:
                    print("Не хватет данных,(subj и date) пустые")

                response['type'] = "homework"
                response['answ'] = hw
            
            elif parameters['type'] == 'library':#В словаре для библиотеки, который приходит ко мне, должен быть ключ typeofbook:учебник или лабник или задачник или всё#
                        sql.execute("SELECT * FROM library ")
                        lib = sql.fetchall()
                        response['type'] = "library"
                        response['answ'] = lib

            elif parameters['type'] == "lection":# Для лекций на показ в словаре  должен быть ключ  typelection: True или False, который даст мне понимание того, нужно ли выводить всё
                if parameters['typelection']:
                    sql.execute("SELECT * FROM lection ")
                    lect = sql.fetchall()
                elif parameters['typelection'] is not True:#Здесь если нужно вывести только определенные лекции с номером или по просто определенному предмету 
                        if parameters['num'] is None:#ВАЖНО! пользователь в этом случае обязательно должен ввести как минимум семестр и предмет
                            sql.execute("SELECT * FROM lection WHERE subj = ? and  semestr = ?", (parameters['subj'], parameters['semestr']))  
                            lect = sql.fetchall()
                        elif parameters['num'] is  not None:
                            sql.execute("SELECT * FROM lection WHERE subj = ? and  semestr = ? and num = ?", (parameters['subj'], parameters['semestr'],  parameters['num']))  
                            lect = sql.fetchall()


                        response['type'] = "library"
                        response['answ'] = lect

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

    


