# -*- coding: utf-8 -*-

import pymysql
from elasticsearch import Elasticsearch
import json
from collections import defaultdict
import numpy as np
import requests
import argparse


def insert_es():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_index', type=int)
    parser.add_argument('end_index', type=int)
    args = parser.parse_args()
    start_index = args.start_index
    end_index = args.end_index

    es = Elasticsearch(["localhost:9200"])
    # if start_index == -1:
    # es.indices.delete(index="so_190601", ignore=[400, 404])
    conn = pymysql.connect(host='localhost', port=3306, user='visit', password='123456', db='stackoverflow_190603',
                           charset='utf8')
    with conn.cursor() as cursor:
        for index in range(start_index, end_index, 1000):
            right_index = min(index + 1000, end_index)
            print(index, right_index)
            sql = 'select * from questions where `Id` >= {} and `Id` < {}'.format(index, right_index)
            cursor.execute(sql)
            results = cursor.fetchall()
            for i in results:
                Id, AcceptedAnswerId, CreationDate, Score, ViewCount, Body, OwnerUserId, OwnerDisplayName, \
                LastEditorUserId, LastEditorDisplayName, LastEditDate, LastActivityDate, Title, Tags, AnswerCount, \
                CommentCount, FavoriteCount, ClosedDate, CommunityOwnedDate = i
                CreationDate_str = CreationDate.strftime("%Y-%m-%d %H:%M:%S")
                Body = Body if Body else ''
                OwnerUserId = OwnerUserId if OwnerUserId else -32768
                OwnerDisplayName = OwnerDisplayName if OwnerDisplayName else ''
                Title = Title if Title else ''
                Tags = Tags if Tags else ''
                record = {'Id': Id, 'CreationDate': CreationDate_str, 'Score': Score, 'ViewCount': ViewCount,
                          'Body': Body, 'OwnerUserId': OwnerUserId, 'OwnerDisplayName': OwnerDisplayName,
                          'Title': Title, 'Tags': Tags, 'AnswerCount': AnswerCount}
                es.index(index="so_190601", doc_type="question", body=record, id=Id, request_timeout=30)
    conn.close()


if __name__ == '__main__':
    insert_es()
