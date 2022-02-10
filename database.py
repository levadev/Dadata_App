import sqlite3

#Set of setings
SETTINGS = {
        'URL' : 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address',
        'API' : '',
        'lang' : 'ru'
    }

#The function connect to SQL Database
def sql_connection():
    connect = sqlite3.connect('settingsDaDataApp.db')
    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS settingsDaDataApp(
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            URL TEXT,
                            API TEXT,
                            lang TEXT
                    )''')

    cursor.execute('SELECT * FROM settingsDaDataApp')

    if cursor.fetchone() == None:
        cursor.execute("INSERT INTO settingsDaDataApp VALUES(?, ?, ?, ?)", (None , SETTINGS['URL'], SETTINGS['API'],  SETTINGS['lang']))
        connect.commit()

    return connect

#The function requests settings from database and returns dictionari of current settings
def get_settings(connect):
  cursor = connect.cursor()
  cursor.execute('SELECT * FROM settingsDaDataApp')
  data = cursor.fetchone()
  return         {
            'id' : data[0],
            'URL' : data[1],
            'API' : data[2],
            'lang' : data[3]
        }

#The function updates current settings from Dadata.change() function
def update_settings(connect, settings:dict):
    cursor = connect.cursor()
    for key, value in settings.items():
        cursor.execute(f"UPDATE settingsDaDataApp SET '{key}' = ? WHERE id = ?", (value, 1))
    
    connect.commit()

connect = sql_connection()