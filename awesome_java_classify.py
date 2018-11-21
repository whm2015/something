# -*- coding: utf-8 -*-

import requests
import Levenshtein
from bs4 import BeautifulSoup
from collections import OrderedDict


def main():
    a = requests.get('https://github.com/akullpp/awesome-java#resources')
    soup = BeautifulSoup(a.text, "html5lib")
    classify = OrderedDict()
    project = soup.find('a', id='user-content-projects')
    class_name = ''
    for i in project.parent.find_next_siblings():
        if i.name == 'h2':
            break
        elif i.name == 'h3':
            class_name = i.text.strip()
        elif i.name == 'ul':
            for j in i.find_all('li'):
                classify[j.a.text] = class_name.strip()
    for i in classify.items():
        print(i)
    with open('C:\\Users\\isaac\\Desktop\\classify.txt', 'w') as f:
        for i in classify.items():
            f.write(i[0]+':'+i[1]+'\n')

if __name__ == '__main__':
    main()
