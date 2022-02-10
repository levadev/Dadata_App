import os
os.system('pip install -r ./requirements.txt')
import shutil
import database
import service


#<------------------ Function ------------------>
#Several main functions

def clean_console():
    os.system('cls')
    print('\t\t\t\t\t\t\t\t\t\tDaData Suggest App')


def remove_temporary_files():
    """
    :return: None
    :todo: remove __pycache__ file from the directory, if files is not in directory then returns None
    """
    
    try:
        shutil.rmtree('./__pycache__')
    except Exception as e: 
        print(f'Упс, что-то не так :( --> {e}')
        return None


def get_coordinates(address):
    """
    :param address: address what you find
    :type address: str
    :return: string coordinates
    :todo: get a coordinates from the addres, if is exist then returns coordinates
    """
    
    settings = database.get_settings(database.connect)
    response = service.make_response(settings, dict(query=address, language=settings['lang']))
    response = response[0]['data']

    if response['geo_lat'] and response['geo_lon'] is not None:
        return f"Широта: {response['geo_lat']},         Долгота: {response['geo_lon']}"
    
    else:
        return "Похоже, что не удалось определить точные координаты"


#The function makes (returns) a menu that specifies the action for the user
def sure_menu(text):
    """
    :param text: text to be displayed
    :type text: str
    :return: dictionary menu that specifies the action for the user
    :todo: makes a menu that specifies the action for the user
    """
    
    return {
        'name' : text,
        'items' : [
            ['изменить', lambda: True],
            ['не менять', lambda: False]
        ] 
    }


def change(what, key, value):
    """
    :param what: What are you change?
    :type what: str
    :param key: key of settings in database
    :type key: str
    :param value: new value
    :return: 0
    :todo: change a settings
    """
    
    clean_console()
    
    try:
        sure = show_menu(sure_menu(f'Вы уверены, что хотите изменить {what}?'), True)

        if sure:
            database.update_settings(database.connect, {key: value})
            clean_console()
            print('Настройки настроены! :)')

        return 0

    except Exception as e: 
        print(f'Упс, что-то не так :( --> {e}')


def menu_request():
    """
    :todo: make a request to the address entered by the user and returns chosen coordinates
    """

    clean_console()
    settings = database.get_settings(database.connect)
    if settings['API'] == '':
        print('Чтобы пользоваться этой функцией нужно ввести публичный API токен')
        change('API', 'API', input('Пожалуйста, введите API: '))
        settings = database.get_settings(database.connect)
    
    address = input('Что вы хотите найти? --> ')
    response = service.make_response(settings, dict(query=address, language=settings['lang']))
    addresses = ['выбрать ' + item['unrestricted_value'] for item in response]

    if len(addresses) == 0:
        print('Похоже, что такого адреса не нашлось, пожалуйста, попробуйте перефразировать запрос')
    
    else: 
        #Defenition of the text for user
        rslt = 'результат' if len(addresses) == 1 else 'результата' if len(addresses) in range(2,4) else 'результатов'
        
        address_menu = {
            'name': f'\n\nПо вашему запросу нашлось {len(addresses)} {rslt} :',
            'items': [[item,
                            lambda: print(f"Координаты для вашего адреса: {get_coordinates(item[8:])}")
                        ] for item in addresses]
        } 
        
        address_menu['items'].append(['выйти', lambda: 0])
        show_menu(address_menu, False)



#<------------------ Data ------------------>
#Settings menu
SET = {
    'name' : '\t\t\t\t\t\t\t\Пользовательские настройки',
    'items' : [
        ['изменить URL', lambda: change('URL', 'URL', input('Пожалуйста, введите URL: '))],
        ['изменить API', lambda: change('API', 'API', input('Пожалуйста, введите API: '))],
        ['изменить язык', lambda: show_menu(LANGUAGE, True)],
        ['сбросить настройки', lambda: database.update_settings(database.connect, database.settings) if show_menu(sure_menu('Вы уверены, что хотите вернуть настройки по-умолчанию?')) else 0],
        ['вернуться назад', lambda: 0]
    ]
}

#Language menu
LANGUAGE = {
    'name' : '\t\t\t\t\t\t\t\Меню выбора языка',
    'items' : [
        ['поменять язык на русский', lambda: change('язык', 'lang', 'ru')],
        ['поменять язык на английский', lambda: change('язык', 'lang', 'en')],
        ['вернуться назад', lambda: 0]
    ]
}

#Start menu
START = {
      'name' : '\t\t\t\t\t\t\t\Главное меню',
      'items' : [
          ['узнать координаты по адресу', lambda: menu_request()],
          ['войти в меню настроек', lambda: show_menu(SET,True)],
          ['выйти из приложения', lambda: 0]
      ]
}



#<------------------ Application ------------------>
#The function make the interface of the Application
def show_menu(menu, turn):
    """
    :param menu: dictionary of menu
    :type menu: dict
    :param turn: bolean statment
    :type turn: bolean
    :todo: make the interface of the Application
    """
    
    state = True

    while state:

        if turn:
            clean_console()
        
        print(menu['name'])

        for i, item in enumerate(menu['items']):
            print(f'Введите {i+1} чтобы {item[0]}')

        try:
            inp = input('Пожалуйста, введите номер нужного пункта меню: ')
            
            if str.isnumeric(inp) and int(inp) > 0:
                    inp = int(inp) 
                    item = menu['items'][inp-1]
                    rslt = item[1]()

                    if turn:
                        if rslt is None:
                            continue
                        
                        elif rslt == 0:
                            remove_temporary_files()
                            break

                        else:
                            state = False
                            return rslt

                    if rslt == 0:
                        remove_temporary_files()
                        break
            else:
                raise Exception('Можно вводить только номера пунктов меню...')

        except Exception as e: 
            print(f'Упс, что-то не так :( --> {e}')

if __name__ == '__main__':
    show_menu(START,True)
