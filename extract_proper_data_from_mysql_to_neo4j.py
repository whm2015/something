# coding: utf-8

import csv
from csv import Dialect
import pandas

def do(read_file, write_file, extract_index, whole=False):
    with open(read_file) as r_f:
        with open(write_file, 'w') as w_f:
            for index, i in enumerate(r_f):
                one_line = i.strip().split(',')
                extract_line = [one_line[x] for x in extract_index]
                if '\\N' not in extract_line:
                    if whole:
                        w_f.write(i)
                    else:
                        w_f.write(','.join(extract_line) + '\n')
                if index > 100:
                    break


def language_add_column_identify_ID():
    #already done
    pass


def do_special(read_file, write_file, extract_index):
    # handle some comlicated csv which has text with '\' in value
    # but there's no need to really handle the text, just make they in right position
    # and extract number values
    # so values located in extract_index must be number or '\N'(null)
    a = pandas.read_csv(read_file, escapechar='\\', header=None, chunksize=3, iterator=True)
    with open(write_file, 'w') as w_f:
        for one_chunk in a:
            for row_index, row in one_chunk.iterrows():
                extract_line = [str(row.iat[x]) for x in extract_index]
                if 'N' not in extract_line:
                    w_f.write(','.join(extract_line) + '\n')


if __name__ == '__main__':
    in_file = ["issues.csv", "issues.csv", "issues.csv", "projects.csv", "pull_requests.csv",
               "commits.csv", "pull_request_history.csv"]
    out_file = ["issue_assignee.csv", "issue_ispr.csv", "issue_reporter.csv", "project_fork.csv",
                "pull_requests_headbase.csv", "commits_belong.csv", "pull_request_history_prevent.csv"]
    index = [(0,3), (0,5), (0,2), (0,7), (3,4), (0,4), (1,4)]
    # for i in range(6):
    #     do(in_file[i], out_file[i], index[i])
    # do(in_file[6], out_file[6], in_file[6], True)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('max_colwidth', 100)
    do_special(r'C:\Users\王惠民\Desktop\testtest.csv', r'C:\Users\王惠民\Desktop\testout.csv', (0,4))