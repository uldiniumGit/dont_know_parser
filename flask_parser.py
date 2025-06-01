from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/contacts/')
def contacts():
    developer_name = 'uldinium'
    creation_date = '25.01.23'
    return render_template('contacts.html', name=developer_name, creation_date=creation_date)


@app.route('/results')
def results():
    url = 'https://lenta.ru/parts/news/'

    response = requests.get(url)
    response.raise_for_status()  # Проверяем, что запрос успешный

    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.find_all('li', class_='parts-page__item')

    # Удаляем последний элемент — "Показать еще"
    if items:
        items.pop()

    news_list = []

    for item in items:
        link_tag = item.find('a')
        if not link_tag:
            continue

        # Заголовок новости
        title_tag = link_tag.contents[0] if link_tag.contents else None
        title = title_tag.string.strip() if title_tag and title_tag.string else "Без заголовка"

        # Время новости
        time_str = "Нет времени"
        if len(link_tag.contents) > 1:
            second_child = link_tag.contents[1]
            if hasattr(second_child, 'contents') and len(second_child.contents) > 0:
                time_tag = second_child.contents[0]
                if time_tag and time_tag.string:
                    time_str = time_tag.string.strip()

        href = link_tag.get('href', '')
        full_url = href if href.startswith('http') else 'https://lenta.ru' + href

        news_list.append({
            'title': title,
            'time': time_str,
            'url': full_url
        })

    return render_template('results.html', news_list=news_list)


@app.route('/run', methods=['GET'])
def run_get():
    return render_template('run.html')


text_list = []


@app.route('/run', methods=['POST'])
def run_post():
    text = request.form.get('input_text', '').strip()
    if text:
        text_list.append(text)
    return render_template('run.html', text_list=text_list)


if __name__ == "__main__":
    app.run(debug=True)

