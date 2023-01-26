from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/contacts/')
def contacts():
    # Где-то взяли данные
    # Контекст name=developer_name - те данные, которые мы передаем из контроллера в шаблон
    # Словарь контекста
    developer_name = 'uldinium'
    # context = {'name': developer_name}
    return render_template('contacts.html', name=developer_name, creation_date='25.01.23')


@app.route('/results')
def results():
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
            href_list.append('https://lenta.ru' + p)

    list_counter = []
    for i in range(len(news_list)):
        list_counter.append(i)
    news_list_01 = []
    for i in range(len(news_list)):
        news_list_01.append(news_list[i] + ' ' + time_list[i])
        news_list_01.append(href_list[i])
        # news_list_01.append()
    return render_template('results.html', news_list_01=news_list_01, list_counter=list_counter)


@app.route('/run', methods=['GET'])
def run_get():
    return render_template('run.html')


text_list = []


@app.route('/run', methods=['POST'])
def run_post():
    # Как получить данные формы
    text = request.form['input_text']
    text_list.append(text)
    return render_template('run.html', text_list=text_list)


if __name__ == "__main__":
    app.run(debug=True)
