# coding:utf-8

import sys
import requests
import pymysql
from collections import OrderedDict
from bs4 import BeautifulSoup


def main():
    downloads = [
        'Badges', 'Comments', 'Posts', 'Tags', 'Users',
        # 'PostLinks', 'Votes', 'PostHistory',
                 ]
    url = 'https://data.stackexchange.com/stackoverflow/query/new'
    page_content = requests.get(url)
    r = BeautifulSoup(page_content.content, 'html5lib')
    tables = r.find('span', attrs={'class': 'heading'}).find_next_sibling('ul')
    dataset = OrderedDict()
    for i in tables.find_all('li'):
        table_name = i.span.string.strip()
        table_schema = OrderedDict()
        field_names = [x.string.strip() for x in i.dl('dt')]
        fields_types = [x.string.strip() for x in i.dl('dd')]
        for name, _type in zip(field_names, fields_types):
            if _type == 'nvarchar (max)':
                _type = 'LongText'
            table_schema[name] = _type
        dataset[table_name] = table_schema
    print(dataset)
    db = pymysql.connect(
        host="10.1.1.61", user="root", password="123456", db="stackoverflow_181202", port=36810, charset='utf8')
    for i in dataset.items():
        if i[0] in downloads:
            sql = "create table {table_name}({table_schema})CHARSET=utf8;".\
                format(table_name=i[0], table_schema=','.join([' '.join(x) for x in i[1].items()]))
            print(sql)
            cursor = db.cursor()
            cursor.execute(sql)
    db.close()


if __name__ == '__main__':
    main()