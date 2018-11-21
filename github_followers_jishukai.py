#coding:utf-8

import pymysql
import requests
import csv
import sys
import json
import time


def get_cooccurrence_user_followers(output_file):
    db = pymysql.connect("10.1.1.61", "visitor", "visitor", "stackoverflow_github", 36810)
    cursor = db.cursor()
    cursor.execute("select user_id, count(1) from ghtorrent_restore.followers "
                   "where user_id in "
                   "(select id from ghtorrent_restore.users ) "
                   "group by user_id")
    data = cursor.fetchall()
    with open(output_file, 'w') as f:
        for i in data:
            f.write(str(i) + '\n')
    db.close()


def get_followers_of_user_from_jishukai(csv_file, output_file):
    count = 0
    a = list()
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        proxies = {'http': 'http://localhost:9666', 'https': 'http://localhost:9666'}
        h = {'Authorization': 'token 2e2c7fa0de6885ead0c0d9a8ea4a1b62dd861475'}
        odd_count = 0
        for index, i in enumerate(list(reader)):
            if i[2:10] == ['0', ] * 8 and i[10:23] != ['0', ] * 13:
                odd_count += 1
            # if i[2:23] == ['0', ] * 21:
            #     continue
            # else:
            #     try_time = 4
            #     followers = -2
            #     while 1:
            #         try:
            #             r = requests.get('https://api.github.com/users/' + i[1].strip(), headers=h, proxies=proxies)
            #         except Exception:
            #             r.close()
            #             try_time -= 1
            #             if try_time == 0:
            #                 break
            #             time.sleep(1)
            #         else:
            #             if r.status_code != 200:
            #                 followers = -1
            #             else:
            #                 followers = json.loads(r.text)['followers']
            #             r.close()
            #             time.sleep(0.5)
            #             break
            #     print(i[1], followers)
            #     a.append(i[0] + ' ' + i[1] + ' ' + str(followers))
            #     count += 1
    print(count)
    print(odd_count)

    # with open(output_file, 'w') as f:
    #     for i in a:
    #         f.write(i + '\n')


if __name__ == '__main__':
    get_followers_of_user_from_jishukai(
        r'C:\Users\isaac\Desktop\some_data\CoderProfileResults1112_100commit.csv',
        r'C:\Users\isaac\Desktop\some_data\followers.txt')