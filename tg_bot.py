import time
import telebot
from bs4 import BeautifulSoup
import requests
import os

TOKEN = ''  # Вставьте сюда ваш токен

bot = telebot.TeleBot(TOKEN)


# Приветствие
@bot.message_handler(commands=['start'])
def send_welcome(message):
    print('start')
    bot.reply_to(message, "хей")


# Команды помощи
@bot.message_handler(commands=['help'])
def send_help(message):
    print('help')
    bot.reply_to(message,
                 "Список команд:\n"
                 "/start — Приветствие\n"
                 "/help — Все команды\n"
                 "/timer — Запускает таймер на 5 секунд\n"
                 "/news — Новости")


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
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        bot.send_message(message.chat.id, 'Ошибка при получении новостей: ' + str(e))
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('li', class_='parts-page__item')

    if not items:
        bot.send_message(message.chat.id, 'Новости не найдены.')
        return

    # Удаляем последний элемент "Показать еще"
    items.pop()

    for item in items:
        try:
            # Получаем заголовок новости
            title = item.a.get_text(strip=True)

            # Получаем ссылку на новость
            href = item.a['href']
            if not href.startswith('http'):
                href = 'https://lenta.ru' + href

            # Получаем время новости
            time_tag = item.find('time')
            time_text = time_tag.get_text(strip=True) if time_tag else 'Время не указано'

            # Формируем сообщение
            news_message = f"{title}\n{href}\n{time_text}"

            bot.send_message(message.chat.id, news_message, disable_web_page_preview=True)
        except Exception as e:
            print(f"Ошибка при обработке новости: {e}")

# Команда для админа
@bot.message_handler(commands=['restart'], func=lambda message: message.from_user.username == 'Booklee')
def admin_restart(message):
    # Здесь можно добавить команду перезапуска бота или выполнить нужное действие
    bot.reply_to(message, "Перезапуск не реализован.")
    # Пример вызова внешней команды:
    # os.system('notepad')  # Это откроет блокнот, что скорее всего не нужно


# Ответ на текстовые сообщения
@bot.message_handler(content_types=['text'])
def reply_text(message):
    print(message)
    text = message.text
    bot.reply_to(message, f'Сам {text}')


# Ответ на стикер
@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    file_id = 'CAACAgIAAxkBAAO8Y8k9R-1nCwZStuQBBjzyhVaD_ugAAvYAA6bdEgzbFiprLIJvuS0E'
    print(message)
    bot.send_sticker(message.chat.id, file_id)


# Если хотите использовать команду с параметром, раскомментируйте и отредактируйте
# @bot.message_handler(commands=['say'])
# def say(message):
#     print('say')
#     text = ' '.join(message.text.split(' ')[1:])
#     bot.reply_to(message, text.upper())


bot.infinity_polling()

