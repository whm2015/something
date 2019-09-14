# -*- coding: utf-8 -*-

import re
import sys
import csv
import json
import requests
import pymysql
import time
from bs4 import BeautifulSoup
from py2neo import Graph


def get_most_stars_project():
    # use github api search projects ordered by stars
    # return id, href(important), stars
    h = {'Authorization': 'token c9848e23704d3366e8235ccd472bacc7086361b4'}
    this_turn = set()
    projects = []
    iter_time = 3
    page = 'https://api.github.com/search/repositories?q=stars%3A%3E%3D10000&sort=stars&order=desc&per_page=100'
    while iter_time > 0:
        iter_time -= 1
        r = requests.get('https://api.github.com/rate_limit', headers=h)
        rate_limit = json.loads(r.text)
        print(rate_limit['resources']['search'])
        search_remain = rate_limit['resources']['search']['remaining']
        if search_remain < 1:
            search_re_time = rate_limit['resources']['search']['reset']
            print('睡到:'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(search_re_time)))
            now_time = time.time()
            time.sleep(search_re_time-now_time+1)
        r = requests.get(page, headers=h)
        page_content = json.loads(r.text)
        for i in page_content['items']:
            _id = i['id']
            full_name = i['full_name']
            if _id in this_turn:
                continue
            print(full_name)
            this_turn.add(_id)
            stars = i['stargazers_count']
            projects.append([str(_id), full_name, str(stars)])
        page_indexes = re.split(r'[<>]', r.headers['Link'])
        for _index, i in enumerate(page_indexes):
            if 'rel="next"' in i:
                break
        page = page_indexes[_index-1]
        print(page)

    with open('projects.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(projects)


def match_id_according_url():
    # use mysql first, if mysql returns none(mysql was a bit old), then use neo4j
    # may miss some newly rising project(that project is awesome, rising within 6 month)
    # mysql:2018-07, neo4j:2018-10, sort time:2019-01

    db = pymysql.connect("10.1.1.61", "visitor", "visitor", "ghtorrent_restore", 36810)
    #graph = Graph(host='10.1.1.4', username='neo4j', password='buaaxzl')
    cursor = db.cursor()
    _href_stars_id = []
    not_has = []
    with open('projects.csv') as f:
        reader = csv.reader(f)
        for i in reader:
            print(i)
            if not i[1].startswith('/'):
                i[1] = '/' + i[1]
            cursor.execute('select id from projects '
                           'where url = "https://api.github.com/repos{_href}" '
                           'and deleted=0 '
                           # 'and forked_from is null' # 这里有问题。有的项目状态是deleted，但是只有那一条能搜到
                           .format(_href=i[1]))
            data = cursor.fetchall()
            if data:
                _id = data[0][0]
            else:
                print('not mysql:' + i[1])
                # data = graph.run('match (a:Project) '
                #                  'where a.url =~ "(?i)https://api.github.com/repos{_href}" '
                #                  # 'and a.forked_from is null '
                #                  'and a.deleted=0 return a.projectId'
                #                  .format(_href=i[1])).data()
                # if data:
                #     _id = data[0]['a.projectId']
                # else:
                #     print('not neo4j:' + i[1])
                #     not_has.append(i[1])
                #     continue
            _href_stars_id.append([i[1], str(i[2]), str(_id)])
    db.close()
    print(len(not_has))
    with open('projects_id.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(_href_stars_id)


def main():
    db = pymysql.connect("39.105.65.95", "root", "cooper@2018", "sdpweb", 3306)
    cursor = db.cursor()
    with open('projects_id.csv') as f:
        reader = csv.reader(f)
        for i in reader:
            print(i)
            pid = i[2].split()[0]
            stars = i[1]
            cursor.execute('insert into gh_repo_ranks values({0},{1})'.format(pid, stars))
    db.commit()
    db.close()


def count():
    a = set()
    with open('projects.csv') as f:
        reader = csv.reader(f)
        for i in reader:
            a.add(i[1])
    return a


if __name__ == '__main__':
    main()