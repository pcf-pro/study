r"""
Usage example
for help
$ python parsed.py -h


"""
import psycopg2
import requests as rq
from bs4 import BeautifulSoup
import argparse


def find_items():
    zapros = rq.get('http://feeds.reuters.com/reuters/topNews')
    text = zapros.text
    soup = BeautifulSoup(text, 'xml')
    items = soup.findAll('item')
    return items


def parse_to_screen(items):
    for line in items:
        print(line.title.text, line.pubDate.text, sep='\n')
        fre = line.description.text
        if "div" in fre:
            print(fre[:fre.index('div') - 1])
        print(line.link.text)
        print()


def parse_to_csv(items):
    with open("TopNew.csv", "a") as csv_file:
        for line in items:
            fre = line.description.text
            if "div" in fre:
                z = fre[:fre.index('div') - 1]
            csv_file.write(line.title.text + " " + line.pubDate.text + " " + z + " " + line.link.text + '\n')
        print('File TopNews is greate!')


def parse_to_db(items):
    # try:
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
        for line in items:
            # cur = con.cursor()
            fre = line.description.text
            if "div" in fre:
                zte = fre[:fre.index('div') - 1]
            t1 = line.title.text
            t2 = line.pubDate.TEXT
            t3 = line.link.text

            cur.execute("INSERT INTO TOPNEWS(id, daty, title, descri, yrel)  VALUES (default, %s, %s, %s, %s)",
                        [t2, t1, zte, t3])
    qu = input('Вывести все записанное в таблицу? (да/нет)')
    if qu == 'да':
        cur.execute("""SELECT id, daty, title, descri, yrel FROM TOPNEWS""")
        rows = cur.fetchall()
        for row in rows:
            print("ID = {} ".format(row[0]))
            print("daty = {}".format(row[1]))
            print("title = {}".format(row[2]))
            print("descri = {}".format(row[3]))
            print('yrel = {}'.format(row[4]))
    else:
        con.commit()
        con.close()


# except psycopg2.DatabaseError:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--parse_print", required=False, action="store_true", help='Вывести на экран')
    parser.add_argument("--parse_csv", required=False, action="store_true")
    parser.add_argument("--parse_db", required=False, action="store_true")

    args = parser.parse_args()

    if args.parse_print:
        items_ = find_items()
        parse_to_screen(items_)

    elif args.parse_csv:
        items_ = find_items()
        parse_to_csv(items_)
    elif args.parse_db:
        items_ = find_items()
        parse_to_db(items_)
