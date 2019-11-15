r"""
Usage example
for help
$ python Parser list-habr.py -h
"""

import argparse

import requests as rq
from bs4 import BeautifulSoup


def listorg(a='4868135'):  # парсер для листорг сохраняется в таблицу
    # with open('C:/index.html', encoding='utf-8') as fp:
    #     soup = BeautifulSoup(fp, 'xml')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    zapros = rq.get('https://www.list-org.com/company/' + a, headers=headers)
    soup = BeautifulSoup(zapros.text, 'xml')
    items = soup.findAll('div', class_='c2m')  # ищем блок див с классом с2м - там лежит таблица
    result = [soup.p.text, ": ".join(soup.table.tr.text.split(':'))]  # для вывода результата
    temp = soup.table.text.split()  # перем первый блок и сплитим - там есть статус, регистрация и кпп и инн
    for i in range(len(temp)):  # проходим циклом и проверяем на наличии нужного слова в листе, если есть добавляем
        if 'регистрации' in temp[i]:
            result.append('Дата регистрации: ' + temp[i][temp[i].index('регистрации:') + 12:])
        elif 'Статус' in temp[i]:
            result.append(": ".join(temp[i].split(':')))
        elif 'КПП' in temp[i]:
            result.append('ИНН: ' + temp[i][temp[i].index('КПП:') + 4:])
        elif 'Уставной' in temp[i]:
            result.append('КПП: ' + temp[i - 1])
    rter = items[-1].text.split()
    result.append('ОГРН: ' + "".join(rter[rter.index("ОГРН") + 1:rter.index('и')]))  # и последний пукт ОГРН
    with open("list-org.csv", "a") as csv_file:
        for line in result:
            csv_file.write(line + '\n')
        print('File list-org is greate!')


def habr():  # вызов парсера для хабра
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    zapros = rq.get('https://habr.com/ru/top/yearly/', headers=headers)
    soup = BeautifulSoup(zapros.text, 'lxml')
    result = {}
    # with open('C:/index.html', encoding='utf-8') as fp:
    #     soup = BeautifulSoup(fp, 'lxml')
    body_new = soup.findAll('div', class_="post__body post__body_crop")  # ищем контейнеры дива с классом поста
    title = soup.findAll('h2', class_='post__title')  # ищем х2 именно там хранится заголовок
    name_date = soup.findAll('header', class_='post__meta')  # ищем голову, где автор + дата

    for i in range(len(title)):  # запускаем цикл для краткого заголовка и добавляем в словарь предварительно очистив
        if title[i].find(class_='post__title_link') is not None:
            result[title[i].text.strip()] = []

    for i in range(len(body_new)):  # цикл для обработки и очистки тела новости дополнительно заворачиваем в лист
        if body_new[i].find('div', class_='post__text post__text-html js-mediator-article') is not None:
            result[title[i].text.strip()].append(
                [body_new[i].text.strip().replace('\n', '').replace('Читать дальше →', '')])

    for i in range(len(name_date)):  # цикл для автора и даты, так же оборачиваем в лист
        if name_date[i].find('span', class_='user-info__nickname user-info__nickname_small') is not None:
            result[title[i].text.strip()].append(name_date[i].text.strip().replace('\n', '').split('\n'))

    print('Получено:', len(result), 'новостей.')

    with open("harb.csv", "a") as csv_file:  # записываем все в файл, или создавая его или дописывая в сущесвтующий
        csv_file.write('Получено: ' + str(len(result)) + ' новостей.\n')
        for line in result.keys():
            csv_file.write(line + ' ' + str(*result[line][0]) + ' ' + str(*result[line][1]) + '\n')
        print('File habr is greate!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Скрип для парсинга сайта по заданным параметрам',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--listorg", required=False, action="store_true",
                        help=' Сохранить таблицу в формате .csv')
    parser.add_argument("--habr", required=False, action="store_true", help='Сохранить таблицу в формате .csv')
    parser.add_argument('--number', required=False,
                        help='Указать дополнительный индекс страницы. (--listorg --number=982773)',
                        type=str, default='4868135')

    args = parser.parse_args()

    if args.listorg:
        listorg(args.number)

    elif args.habr:
        habr()
