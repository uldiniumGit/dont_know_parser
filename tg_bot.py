import time
import telebot
from bs4 import BeautifulSoup
import requests
import os
import sys

TOKEN = ''

bot = telebot.TeleBot(TOKEN)


# Приветствие
@bot.message_handler(commands=['start'])
def send_welcome(message):
    print('start')
    bot.reply_to(message, "хей")


# Команды
@bot.message_handler(commands=['help'])
def send_welcome(message):
    print('help')
    bot.reply_to(message,
                 "Список команд:\n/start Приветствие\n/help Все команды"
                 "\n/timer Запускает таймер на 5 секунд\n/news Новости")


# Таймер
@bot.message_handler(commands=['timer'])
def timer(message):
    print('timer')
    for i in range(5):
        time.sleep(1)
        bot.send_message(message.chat.id, i + 1)


# Новости
@bot.message_handler(commands=['news'])
def news(message):
    print('news')

    url = 'https://lenta.ru/parts/news/'

    response = requests.get(url)

    # Создаем суп для разбора html
    soup = BeautifulSoup(response.text, 'html.parser')

    first = soup.find_all('li', class_='parts-page__item')

    # Последним элементом лежит показать еще, а не новость. Убираем его.
    first.pop()

    # Листы для новости, времени и ссылки на новость
    news_list = []
    time_list = []
    href_list = []

    # Заполняем листы данными
    for i in first:
        p = i.contents[0].contents[0]
        news_list.append(p.string)

        p = i.contents[0].contents[1].contents[0]
        time_list.append(p.string)

        p = i.contents[0].get('href')

        # Если ссылка на ленту ру, то приводим ее в нужный вид
        if p[0] == 'h':
            href_list.append(p)
        else:
            href_list.append('https://lenta.ru'+p)

    # Выводим сообщения с новостями
    for i in range(len(news_list)):

        # Собираем новость из листов
        news_list_01 = str(news_list[i] + '\n' + href_list[i] + '\n' + time_list[i])
        # Отправляем новость пользователю
        bot.send_message(message.chat.id, news_list_01, disable_web_page_preview=True)


# Команда для админа
@bot.message_handler(commands=['restart'], func=lambda message: message.from_user.username == 'Booklee')
def admin_restart(message):
    os.system('notepad')


# Ответ на сообщение
@bot.message_handler(content_types='text')
def reverse_text(message):
    print(message)
    text = message.text
    bot.reply_to(message, f'Сам {text}')


# Ответ на стикер
@bot.message_handler(content_types='sticker')
def send_sticker(message):
    file_id = 'CAACAgIAAxkBAAO8Y8k9R-1nCwZStuQBBjzyhVaD_ugAAvYAA6bdEgzbFiprLIJvuS0E'
    print(message)
    bot.send_sticker(message.chat.id, file_id)


# Обработка команд с параметром

# @bot.message_handler(commands=['say'])
# def say(message):
#     print('say')
#     text = ' '.join(message.text.split(' ')[1:])
#     bot.reply_to(message, f'{text.upper()}')


bot.infinity_polling()
