from bs4 import BeautifulSoup
import requests

url = 'https://lenta.ru/parts/news/'


response = requests.get(url)

# Создаем суп для разбора html
soup = BeautifulSoup(response.text, 'html.parser')

# print(soup.a)
#
# print(soup.a.string)
#
# print(soup.a.get('href'))

first = soup.find_all('li', class_='parts-page__item')

# Последним элементом лежит показать еще, а не новость. Убираем его.
first.pop()


for i in first:
    p = i.contents[0].contents[0]
    print('Новость:')
    print(p.string)

    p = i.contents[0].contents[1].contents[0]
    print('Время:', p.string)

    p = i.contents[0].contents[1].contents[1]
    print('Тег:', p.string)

    p = i.contents[0].get('href')
    print('https://lenta.ru'+p, '\n')



