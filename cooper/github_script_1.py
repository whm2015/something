import pymysql
from elasticsearch import Elasticsearch
import json
from collections import defaultdict
import numpy as np
import requests

headers = {
    'Content-Type': 'application/json',
}

all_lan = []
with open(
        'D:\\eclipse-workspace\\cooper\\show\\act\\src\\main\\resources\\static\\data\\stackoverflow\\all_languages.txt') as f:
    for i in f.readlines():
        all_lan.append(i.strip().replace('.', '*'))
    print(all_lan)

def get_max_score():
    conn = pymysql.connect(host='10.1.1.62', port=36822, user='visitor', password='visitor', db='stackoverflow_190603',
                           charset='utf8')
    score_max = defaultdict(int)
    all_number = 0
    with conn.cursor() as cursor:
        for index in range(-1, 11588774 + 1, 1000):
            if index // 1000 % 10 == 0:
                print(index)
            sql = 'select Card from users where `Id` >= {} and `Id` < {}'.format(index, index + 1000)
            all_number += cursor.execute(sql)
            results = cursor.fetchall()
            for i in results:
                Card_dict = json.loads(i[0])
                skills = Card_dict['Skills']
                for s_name, s_score in skills.items():
                    if s_score > score_max[s_name]:
                        score_max[s_name] = s_score
    print(all_number)
    print(score_max)
    conn.close()
    np.save('score_max.npy', score_max)


def insert_es():
    score_max = np.load('score_max.npy')[()]
    name_diff_p = [x for x in score_max.keys() if '.' in x]
    for name_con in name_diff_p:
        score_max[name_con.replace('.', '*')] = score_max.pop(name_con)
    # es = Elasticsearch(["39.107.118.16:9200"])
    resp = requests.put('http://localhost:9200/your_index/_settings', headers=headers,
                        data='{"index": {"mapping": {"total_fields": {"limit": "10000"}}}}')
    conn = pymysql.connect(host='39.107.118.16', port=3306, user='visit', password='123456', db='stackoverflow_190603',
                           charset='utf8')
    with conn.cursor() as cursor:
        for index in range(-1, 1):
            sql = 'select * from users where `Id` > {} and `Id` < {}'.format(index, index + 5)
            cursor.execute(sql)
            results = cursor.fetchall()
            for i in results:
                Id, Reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, ProfileImageUrl, EmailHash, AccountId, Age, Card = i
                CreationDate_str = CreationDate.strftime("%Y-%m-%d %H:%M:%S")
                LastAccessDate_str = LastAccessDate.strftime("%Y-%m-%d %H:%M:%S")
                WebsiteUrl_no = WebsiteUrl if WebsiteUrl else ''
                Location_no = Location if Location else ''
                country = Location_no
                address = Location_no
                AboutMe = AboutMe if AboutMe else ''
                Views = Views if Views else 0
                UpVotes = UpVotes if UpVotes else 0
                DownVotes = DownVotes if DownVotes else 0
                ProfileImageUrl = ProfileImageUrl if ProfileImageUrl else ''
                url = 'https://stackoverflow.com/users/{}/{}'.format(Id, DisplayName.lower().replace(' ', '-'))
                Card_dict = json.loads(Card)
                skills_origin = Card_dict['Skills']
                name_diff = [x for x in skills_origin.keys() if '.' in x]
                for name_con in name_diff:
                    skills_origin[name_con.replace('.', '*')] = skills_origin.pop(name_con)
                contributions = Card_dict['Contributions']
                collaborations = Card_dict['Communication']
                tagWithValue_ = {}
                tag = {'pl': [], 'others': []}
                for s_name, s_score in skills_origin.items():
                    if s_name in all_lan:
                        tag['pl'].append(s_name)
                    else:
                        tag['others'].append(s_name)
                    s_score = s_score if s_score >= 0 else 0
                    if score_max[s_name] == 0:
                        tagWithValue_[s_name] = 0
                    else:
                        tagWithValue_[s_name] = 100 * s_score / score_max[s_name]
                record = {'userID': Id,
                          'profile': {'name': DisplayName, 'country': country, 'address': address, 'url': url,
                                      'joinDate': CreationDate_str, 'lastAccessDate': LastAccessDate_str,
                                      'aboutMe': AboutMe, 'imageUrl': ProfileImageUrl, 'belongTo': 2,
                                      'websiteUrl': WebsiteUrl_no, 'views': Views, 'upVotes': UpVotes,
                                      'downVotes': DownVotes, 'accountId': AccountId},
                          'skills': {'tag': tag, 'tagWithValue': skills_origin, 'tagWithValue_': tagWithValue_},
                          'contributions': contributions,
                          'collaborations': collaborations}
                print(type(record))
                print(json.dumps(record))
                # es.index(index="so_190601", doc_type="user", body=record, id=Id, request_timeout=30)
    conn.close()


if __name__ == '__main__':
    get_max_score()
