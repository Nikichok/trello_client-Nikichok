import requests
import sys


auth_params = {
    'key': "f2fed639310b086ea9784b2b330845f8", #Введите ваш ключ от trello
    'token': "d851de6eb70bdae9554cdd99d40a33c1b6f12882d1d0dd772156e2e531f2672a" #Введите ваш токен
}


board_id = "5ef99e1d61f2ce7c58750c2f"  # введите id вашей доски
base_url = "https://api.trello.com/1/{}"


def read():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for clm in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + clm['id'] + '/cards', params=auth_params).json()
        print(clm['name'] + ' - {}'.format(len(task_data)))

        
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'] + '\t' + task['id'])


def create(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for clm in column_data:
        if clm['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name': name, 'idList': clm['id'], **auth_params})
            break


def move(name, column_name):
    duplicate_tasks = get_task_duplicates(name)
    if len(duplicate_tasks) > 1:
        print("Задач с таким названием несколько штук:")
        for index, task in enumerate(duplicate_tasks):
            task_column_name = requests.get(base_url.format('lists') + '/' + task['idList'], params=auth_params).json()['name']
            print("Задача №{}\tid: {}\tНаходится в колонке: {}\t ".format(index, task['id'], task_column_name))  
        task_id = input("Пожалуйста, введите ID задачи, которую нужно переместить: ")  
    else:  
        task_id = duplicate_tasks[0]['id']

    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    task_id = None
    for clm in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + clm['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
            if task_id:
                break
        
    for clm in column_data:
        if clm['name'] == column_name:
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': clm['id'], **auth_params})
            break

    
def column(name):
    return requests.post(base_url.format('lists'), data={'name': name, 'idBoard': board_id, **auth_params}).json()


def column_check(column_name):  
    column_id = None  
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()  
    for column in column_data:  
        if column['name'] == column_name:  
            column_id = column['id']  
            return column_id


def get_task_duplicates(task_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    duplicate_tasks = []
    for column in column_data:  
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()  
        for task in column_tasks:  
            if task['name'] == task_name:  
                duplicate_tasks.append(task)  
    return duplicate_tasks


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'column':
        column(sys.argv[2])