from bs4 import BeautifulSoup
import requests as rq
import psycopg2
import re
import csv

def main():
    print('''Добро пожаловать в парсер.
    Выберите пожалуйста один из пунктов меню:
    1) Парсить новости и вывести на экран
    2) Записать пропарсеные новости в csv файл
    3) Записать данные в таблицу постскуюл
    4) Выйти''')
    a = input('Ваш выбор: ')
    if a==r"[1-4]":
        while a==r"[1-4]":
            print('Введите корректную цифру')
            a = input('Ваш выбор: ')
    elif a=='1':
        print('1')
        base()
        return parser()
    elif a=='2':
        print('2')
        base()
        return pars()
    elif a=='3':
        print('3')
        base()
        return tabl()
    elif a=='4':
        print('4')
        return exit()


def base():
    global table
    zapros = rq.get('http://feeds.reuters.com/reuters/topNews')
    text = zapros.text
    soup = BeautifulSoup(text, 'xml')
    table = soup.findAll('item')
    return table



def parser():

    for line in table:
        print(line.title.text , line.pubDate.text, sep = '\n')
        fre = line.description.text
        if "div" in fre:
            print(fre[:fre.index('div')-1])
        print(line.link.text)
        print()

def pars():

    with open("TopNew.csv", "a") as csv_file:
        for line in table:
            fre = line.description.text
            if "div" in fre:
                z = fre[:fre.index('div')-1]
            csv_file.write(line.title.text +" "+ line.pubDate.text +" "+ z +" "+ line.link.text + '\n')
        print('File TopNews is greate!')

def tabl():
    #try:
        con = psycopg2.connect(database='postgres', user='postgres', password='1', port='5432', host='localhost')
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS TOPNEWS(
                                id      INT,
                                daty    TEXT,
                                title   TEXT,
                                descri  TEXT,
                                yrel    TEXT
                        )""")

        print('Greate table')
        if cur.execute("TABLE TOPNEWS") == None:
            for line in table:
                #cur = con.cursor()
                fre = line.description.text
                if "div" in fre:
                    zte = fre[:fre.index('div')-1]
                t1 = line.title.text
                t2 = line.pubDate.TEXT
                t3 = line.link.text

                cur.execute("INSERT INTO TOPNEWS(id, daty, title, descri, yrel)  VALUES (default, %s, %s, %s, %s)",[t2, t1, zte, t3])
        qu = input('Вывести все записанное в таблицу? (да/нет)')
        if qu =='да':
            cur.execute("""SELECT id, daty, title, descri, yrel FROM TOPNEWS""")
            rows = cur.fetchall()
            for row in rows:
                print("ID = {} ".format(row[0]))
                print( "daty = {}".format(row[1]))
                print("title = {}".format(row[2]))
                print("descri = {}".format(row[3]))
                print('yrel = {}'.format(row[4]))
        else:
            con.commit()
            con.close()
    #except psycopg2.DatabaseError:


main()
