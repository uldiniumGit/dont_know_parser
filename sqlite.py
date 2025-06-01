import sqlite3

# Подключение к базе данных (создаст файл, если его нет)
conn = sqlite3.connect('parser.db')
cursor = conn.cursor()

# Создание таблиц (если ещё не созданы)
cursor.execute('''
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag TEXT UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    time TEXT,
    link TEXT,
    tag_id INTEGER,
    FOREIGN KEY(tag_id) REFERENCES tags(id)
)
''')

conn.commit()

# --- Пример выборки всех новостей ---

cursor.execute('SELECT * FROM news')
news_rows = cursor.fetchall()

for row in news_rows:
    # row = (id, title, time, link, tag_id)
    print(f"Заголовок: {row[1]}")
    print(f"Время: {row[2]}")
    print(f"Ссылка: {row[3]}")
    print(f"ID тега: {row[4]}")
    print('---')

print('_' * 50)

# --- Пример выборки новостей по времени ---

cursor.execute('SELECT * FROM news WHERE time=?', ('12:00',))
news_at_noon = cursor.fetchall()
print("Новости с временем 12:00:")
for row in news_at_noon:
    print(row)

print('_' * 50)

# --- Пример выборки с JOIN для вывода новостей с их тегами ---

query = '''
SELECT n.title, n.time, n.link, tg.tag
FROM news n
JOIN tags tg ON n.tag_id = tg.id
'''

cursor.execute(query)
results = cursor.fetchall()

print("Новости с тегами:")
for title, time_, link, tag in results:
    print(f"Заголовок: {title}")
    print(f"Время: {time_}")
    print(f"Ссылка: {link}")
    print(f"Тег: {tag}")
    print()

# Закрываем соединение
conn.close()
