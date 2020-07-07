from trello import TrelloApi

api_key =  "f2fed639310b086ea9784b2b330845f8"
token = "d851de6eb70bdae9554cdd99d40a33c1b6f12882d1d0dd772156e2e531f2672a"
board_id = "5ef99e1d61f2ce7c58750c2f"

trello = TrelloApi(api_key, token)
dictionary = {}
column_dictionary = {}


def read_tasks():
    task_counter = 0
    for column in trello.boards.get_list(board_id):
        column_dictionary[column['name']] = column['id']
        if len(trello.lists.get_card(column['id'])) > 0:
            card_list = []
            for card in trello.lists.get_card(column['id']):
                task_counter += 1
                card_dict = {'id': task_counter, 'card_name': card['name'], 'card_id': card['id']}
                card_list.append(card_dict)
            dictionary[column['name']] = card_list
        else:
            dictionary[column['name']] = []
    for key in dictionary.keys():

        print('\n"{}" - {} tasks now'.format(key, len(dictionary.get(key))))
        cycle_dict = dictionary.get(key)
        if len(dictionary.get(key)) == 0:
            print('\tNo tasks in this list!')
        else:
            for i in cycle_dict:
                print('\t{} - {}'.format(i['id'], i['card_name']))


def menu():
    read_tasks()
    print('\n')
    print('What you want to do?')
    print('1 - create new list')
    print('2 - create new card')
    print('3 - move card')
    print('4 - delete card')
    print('5 - Exit\n')
    choice_menu = int(input('Enter Your choice - '))
    if choice_menu not in range(1, 6):
        return menu()
    elif choice_menu == 1:
        new_list()
    elif choice_menu == 2:
        new_card()
    elif choice_menu == 3:
        move_card()
    elif choice_menu == 4:
        delete_card()
    elif choice_menu == 5:
        exit()


def new_list():
    name = input('Enter new list name - ')
    trello.boards.new_list(board_id, name, pos=99000)
    print('List was created!')
    menu()


def new_card():
    name = input('Enter new card name - ')
    print('\n')
    count = 0
    temp_column_dict = {}
    for key in column_dictionary.keys():
        count += 1
        temp_column_dict[count] = column_dictionary[key]
        print('{} - {}'.format(count, key))
    column = int(input('\nSelect column for insert new card - '))
    if column not in range(1, len(temp_column_dict) + 1):
        new_card()
    else:
        trello.cards.new(name, temp_column_dict[column])
    print('Card was created!\n')
    menu()


def move_card():
    count = 0
    temp_column_dict = {}
    for key in column_dictionary.keys():
        count += 1
        print('{} - {}'.format(count, key))
        temp_column_dict[count] = column_dictionary[key]
    column = int(input('\nSelect column with your card - '))
    if column not in range(1, len(temp_column_dict) + 1):
        move_card()
    else:
        task_counter = 0
        card_dict = {}
        for card in trello.lists.get_card(temp_column_dict[column]):
            task_counter += 1
            print('{} - {}'.format(task_counter, card['name']))
            card_dict[task_counter] = card['id']
        card = int(input('\nSelect your card - '))
        name = card_dict[card]
        count = 0
        for key in column_dictionary.keys():
            count += 1
            print('{} - {}'.format(count, key))
            temp_column_dict[count] = column_dictionary[key]
        column = int(input('\nSelect column to insert your card - '))
        trello.cards.update_idList(name, temp_column_dict[column])
    print('Done \n')
    menu()


def delete_card():
    read_tasks()
    card_id = int(input('Enter card number - '))
    for value in dictionary.values():
        if len(value) == 0:
            continue
        else:
            for i in value:
                if i['id'] == card_id:
                    trello.cards.delete(i['card_id'])
    print('Card was deleted! \n')
    menu()


if __name__ == '__main__':
    menu()