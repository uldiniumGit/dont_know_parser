"""
Из парсера я получаю 4 типа данных: заголовок новости, время новости, теги новости и ссылку на новость.
У меня будет только две таблицы. Одна с тегами, потому что они могут повторяться в новостях,
а вторая с новостью, временем и ссылкой.
Таблица с новостями будет получать данные из таблицы с тегами по внешнему ключу.
"""

import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('parser.db')

# Создаем курсор
cursor = conn.cursor()

cursor.execute('SELECT * from news')

result = cursor.fetchall()

for i in result:
    print(i[1])
    print(i[2])
    print(i[3])
    print(i[4])

print('_' * 50)

cursor.execute('SELECT * from news where time=?', ('12:00',))
print(cursor.fetchall())

print('_' * 50)

query = 'select n.new, n.time, n.link, tg.tag from news n, tags tg'

# Вывести в нормальном виде таблицу скилы + вакансии
cursor.execute(query)
result = cursor.fetchall()

for i in result:
    print(i[0])
    print(i[1])
    print(i[2])
    print(i[3], '\n')
