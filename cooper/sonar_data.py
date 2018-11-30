#coding:utf-8

import requests
import os
import json
import pymysql
import subprocess
import re
import pymongo


git_blame = 'git blame'


def exe_cmd(exe_dir, command, arg=None, sysout=False):
    if command == 'git blame':
        cm = git_blame + ' ' + arg
    if command == '_custom':
        cm = arg
    else:
        print("error")

    child = subprocess.Popen(cm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=exe_dir)

    if sysout:
        return_text = ''
        return_code = child.poll()
        while return_code is None:
            line = child.stdout.readline()
            return_code = child.poll()
            line = line.strip().decode('utf-8')
            return_text += line
            if line:
                print(line)
    else:
        out = child.communicate()
        print(child.stderr.read())
        return_code = child.poll()
        return_text = out[0].decode('utf-8').strip()


    return return_text, return_code


def get_files(rep_dir, file_list=None):
    files = os.listdir(rep_dir)
    for fi in files:
        fi_d = os.path.join(rep_dir,fi)
        if os.path.isdir(fi_d):
            get_files(fi_d, file_list)
        else:
            file_list.append(os.path.join(rep_dir,fi_d))
    return file_list


def get_violation_to_mysql():
    pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    db = pymysql.connect("10.1.1.61", "root", "123456", "cooper", 36810)
    cursor = db.cursor()
    f = open('d:/test111.txt', 'w', encoding='utf-8')
    for one_project in os.listdir(r'D:\act_project\SpringCloud'):
        rep_dir = os.path.join(r'D:\act_project\SpringCloud', one_project)
        if not os.path.isdir(rep_dir):
            continue
        project_file_list = get_files(rep_dir, [])
        for index, i in enumerate(project_file_list):
            split_path = i.split('\\')
            request_argu = split_path[2] + '_' + split_path[3] + '%3A' + '%2F'.join(split_path[4:])
            print(request_argu)
            r = requests.get(
                'http://192.168.3.251:9000/api/issues/search?additionalFields=_all&resolved=false&'
                'componentKeys=' + request_argu + '&s=FILE_LINE&p=1&ps=500')
            if r.status_code != 200:
                continue
            response = json.loads(r.text)
            issues = response['issues']
            if not issues:
                continue
            for j in issues:
                if 'line' not in j or 'textRange' not in j:
                    continue
                f.write(str(issues) + '\n')
                _project = j['project']
                _component = j['component']
                _key = j['key']
                _rule = j['rule']
                _severity = j['severity']
                _line = j['line']
                _startLine = j['textRange']['startLine']
                _endLine = j['textRange']['endLine']
                _tags = ('$').join(j['tags'])
                _type = j['type']
                argument = '-L ' + str(_line) + ',' + str(_line) + ' ' + i
                argument.replace('\\', '/')
                f.write(argument)
                return_text, return_code = exe_cmd(rep_dir, 'git blame', argument)
                f.write(return_text + '\n')
                left_bracket = return_text.find('(')
                right_bracket = return_text.find(')')
                time_string_start = pattern.search(return_text[left_bracket:right_bracket]).span()[0]
                _git_blame = return_text[left_bracket + 1: left_bracket + time_string_start].strip()
                f.write(_git_blame + '\n')
                sql = 'insert into gitlab_all_projects values(' \
                      '"{}", "{}", "{}", "{}", "{}", "{}", {}, {}, {}, "{}", "{}")' \
                    .format(_git_blame, _project, _component, _key, _rule, _severity, _line,
                            _startLine, _endLine, _tags, _type)
                f.write(sql + '\n')
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                    print('???')
    db.close()
    f.close()


def get_edit_lines_to_mysql():
    # execute in server, windows dont has linux command
    '''git log --author="$(git config --get user.name)" --pretty=tformat: --numstat | gawk '{ add += $1 ; subs += $2 ; loc += $1 - $2 } END { printf "added lines: %s removed lines : %s total lines: %s\n",add,subs,loc }' -'''
	pass


def mysql_into_mongodb():
    user_info = {}
    # users_info = {$username: [0,]*8}
    # users_info = {'username':$username, 'analysis':{'addlines':$add, 'removelines':$remove, 'bugs':$bugs,
    #                   'vulnerability':$vul, 'code_smell':$code, 'blocker':$b, 'critical':$c, 'major'$m}}
    db = pymysql.connect("10.1.1.61", "visitor", "visitor", "cooper", 36810)
    cursor = db.cursor()

    sql1 = 'select username, sum(addLines), sum(removeLines), sum(totalLines) from gitlab_all_users ' \
           'group by username order by username;'
    cursor.execute(sql1)
    results = cursor.fetchall()
    for row in results:
        user_info[row[0]] = [int(row[1]), int(row[2])] + [0,] * 6

    sql2 = 'select git_blame, type, count(1) from gitlab_all_projects group by git_blame, type;'
    cursor.execute(sql2)
    results = cursor.fetchall()
    for row in results:
        if row[1] == 'BUG':
            user_info[row[0]][2] = int(row[2])
        elif row[1] == 'CODE_SMELL':
            user_info[row[0]][3] = int(row[2])
        elif row[1] == 'VULNERABILITY':
            user_info[row[0]][4] = int(row[2])
        else:
            print('error!')

    sql3 = 'select git_blame, severity, count(1) from gitlab_all_projects group by git_blame, severity;'
    cursor.execute(sql3)
    results = cursor.fetchall()
    for row in results:
        if row[1] == 'BLOCKER':
            user_info[row[0]][5] = int(row[2])
        elif row[1] == 'CRITICAL':
            user_info[row[0]][6] = int(row[2])
        elif row[1] == 'MAJOR':
            user_info[row[0]][7] = int(row[2])
        elif row[1] == 'MINOR' or row[1] == 'INFO':
            pass
        else:
            print('error!')
    db.close()
    print(user_info)
    mylist = []
    for _username, _userinfo in user_info.items():
        mylist.append(
            {'username': _username,
             'analysis': {
                 'addlines': _userinfo[0], 'removelines': _userinfo[1],'bug': _userinfo[2],
                 'vulnerability': _userinfo[3], 'code_smell': _userinfo[4],'blocker': _userinfo[5],
                 'critical': _userinfo[6], 'major': _userinfo[7]
                }
             })
    myclient = pymongo.MongoClient('mongodb://192.168.7.113:30000/')
    mydb = myclient["gitlab"]
    mycol = mydb["user_code_analysis"]
    # mycol.insert_many(mylist)

if __name__ == '__main__':
    mysql_into_mongodb()
