import sys
import requests  
  
# Данные авторизации в API Trello  
auth_params = {    
    'key': "f2fed639310b086ea9784b2b330845f8",    
    'token': "d851de6eb70bdae9554cdd99d40a33c1b6f12882d1d0dd772156e2e531f2672a", }  
  
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"

# ID доски, с которой будем работать.
board_id = "5ef99e1d61f2ce7c58750c2f"

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        #print(column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name']+" (задач: " + str(len(task_data)) + ")")
        if not task_data:
          print('\t' + 'Нет задач!')      
          continue      
        for task in task_data:      
          print('\t' + task['name'])  

def create(name, column_name=""):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
	      
    # Проверяем, что передан второй парамметр. Если да, то первый - название задачи, которую нужно создать, а второй - название колонки, в которой должна быть создана задача. Если парамметр один, то это название колонки, которую нужно создать.
    if column_name != "":
    	# Собираем список задач с таким (name) наименованием.
      task_list = []    
      for column in column_data:
          column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
          for task in column_tasks:    
              if task['name'] == name:
                  task_dic = {'id': task['id'], 'name': task['name'], 'name_column': column['name']}
                  task_list.append(task_dic)
      # Если список получился не пустой, выводим его пользователю    
      if len(task_list) > 0:
        print("Задача с таким наименованием уже существует (всего задач " + str(len(task_list)) + "):")
        for i in range(len(task_list)):
        	print(str(i+1) + ". " + task_list[i]['id'] + ", в колонке - " + task_list[i]['name_column']) 
        # Запрашиваем решение о создании еще одной задачи с таким именем
        choice = input("Все-равно создать? (y/N):  ")
        # Если ответ не положительный - заканчиваем выполнение
        if choice.upper() != "Y":
        	print("Задача не создана!!!")
        	return
	    
	    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
      for column in column_data:      
          if column['name'] == column_name:      
              # Создадим задачу с именем _name_ в найденной колонке      
              requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
              break
    else:
      idBoard = column_data[0]['idBoard']
      requests.post(base_url.format('lists'), data={'name': name, 'idBoard': idBoard, **auth_params})

def move(name, column_name):
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_list = []    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:
                task_dic = {'id': task['id'], 'name': task['name'], 'name_column': column['name']}    
                task_list.append(task_dic)    
    # Если задача не найдена, сообщаем об этом
    if len(task_list) == 0:
      print("Задачи " + name + " нет ни в одной колонке")
      return
    # Если найдено больше одной задачи, предалаем выбрать, какую перемещать и присваиваем id выбранной задачи переменной task_id
    elif len(task_list) > 1:
      print("Задач с наименованием " + name + " несколько:")
      for i in range(len(task_list)):
      	print(str(i+1) + ". " + task_list[i]['id'] + ", в колонке - " + task_list[i]['name_column']) 
      choice = int(input("Выберите какую переместить (введите номер строки):  "))
      task_id = task_list[choice - 1]['id']
    
    elif len(task_list) == 1:
      task_id = task_list[0]['id']

    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break

if __name__ == "__main__":
    if len(sys.argv) <= 2:      
      read()      
    elif sys.argv[1] == 'create' :    
      if len(sys.argv) <= 3:
        create(sys.argv[2]) 
      else:
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':    
      move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'card':    
      card(sys.argv[2])

