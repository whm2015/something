# coding: utf-8

import csv
import pandas
import matplotlib.pyplot as mp
import seaborn
import numpy
from collections import OrderedDict
import random
import sys

header = [
    'id', 'login',
    'vio1', 'vio2', 'vio3', 'vio4', 'vio5', 'vio6', 'vio7', 'vio8',
    'api1', 'api2', 'api3', 'api4', 'api5', 'api6', 'api7', 'api8',
    'effe',
    'LOC', 'followers'
    ]


def score_aspect_relative(filename):
    datas = pandas.read_csv(filename, names=header)
    schema = OrderedDict()
    for index, i in enumerate(header):
        if index < 2 or index > 18:
            continue
        column_name = header[index]
        print(column_name)
        schema[column_name] = datas[column_name].tolist()

    # df = datas.iloc[:, 2:18]
    # df = pandas.DataFrame(schema)
    # df_corr = df.corr()
    # # 可视化
    # seaborn.heatmap(df_corr, center=0, annot=True)
    # mp.show()

    # matric = [x[1] for x in schema.items()]
    # covariance_matrix = numpy.cov(matric)
    # # 可视化
    # print(covariance_matrix)
    # seaborn.heatmap(covariance_matrix, center=0, annot=True, xticklabels=header[2:19], yticklabels=header[2:19])
    # mp.show()


def user_score_relative(filename):
    choose = [False, ] + [True, ] * 17 + [False, ] * 2
    datas = pandas.read_csv(filename, names=header, index_col=1)
    ps = []
    count = 0
    special = 0
    for i in range(10000):
        random_2_people = datas.sample(n=2)
        a_followers = random_2_people.iat[0,19] + 2
        b_followers = random_2_people.iat[1,19] + 2
        if not (a_followers/b_followers > 9 or b_followers/a_followers > 9):
            continue
        count += 1
        random_2_people = random_2_people.iloc[:, choose].T
        relativity = random_2_people.corr().iat[0,1]
        if relativity > 0.9:
            # print(random_2_people, relativity)
            special += 1
        ps.append(relativity)
    print(sum(ps)/len(ps))
    print(count)
    print(special)


def something(file):
    # df = pandas.read_csv(file, iterator = True)
    # chunk = df.get_chunk(5)
    # print(chunk)
    with open(file) as f:
        while 1:
            a = f.readline()
            line = int(a.split(',')[0])
            if line%1000000 == 0:
                print(line)
            if line < 367799120:
                continue
            if line > 367799130:
                break
            print(a)

if __name__ == '__main__':
    pandas.set_option('display.max_columns', None)
    something(r'C:\Users\isaac\Documents\NetSarang Computer\6\Xshell\Sessions\commits.csv')