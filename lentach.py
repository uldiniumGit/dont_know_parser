from bs4 import BeautifulSoup
import requests

url = 'https://lenta.ru/parts/news/'

response = requests.get(url)
response.raise_for_status()  # Проверка успешности запроса

soup = BeautifulSoup(response.text, 'html.parser')

items = soup.find_all('li', class_='parts-page__item')

# Последний элемент — это кнопка "Показать ещё", удаляем
if items:
    items.pop()

for item in items:
    # Обходим вложенные элементы более надежно
    link_tag = item.find('a')
    if not link_tag:
        continue

    # Заголовок новости — текст внутри первого дочернего элемента <a>
    title_tag = link_tag.contents[0] if link_tag.contents else None
    title = title_tag.string.strip() if title_tag and title_tag.string else "Нет заголовка"

    # Время новости — внутри второго дочернего элемента <a>, первого дочернего тега внутри него
    time_tag = None
    tag_tag = None
    if len(link_tag.contents) > 1:
        second_child = link_tag.contents[1]
        if hasattr(second_child, 'contents') and len(second_child.contents) >= 2:
            time_tag = second_child.contents[0]
            tag_tag = second_child.contents[1]

    time_str = time_tag.string.strip() if time_tag and time_tag.string else "Нет времени"
    tag_str = tag_tag.string.strip() if tag_tag and tag_tag.string else "Нет тега"

    href = link_tag.get('href', '')
    full_url = href if href.startswith('http') else 'https://lenta.ru' + href

    print('Новость:')
    print(title)
    print('Время:', time_str)
    print('Тег:', tag_str)
    print(full_url)
    print()


