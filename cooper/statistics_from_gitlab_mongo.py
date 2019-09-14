myclient = pymongo.MongoClient("mongodb://39.105.65.95:27017/")
mydb = myclient["gitlab"]

#每个人commit的星期数量
a = defaultdict(lambda : defaultdict(int))
for index, i in enumerate(mydb['commit'].find()):
     a[i['committer_id']][datetime.datetime.strptime(i['created_at'].split('T')[0], "%Y-%m-%d").weekday()] += 1

#每个人不同项目贡献度
user = defaultdict(lambda: defaultdict(int))
pro = defaultdict(int)
for index, i in enumerate(mydb['user'].find()):
    for j, k in i['diffs'].items():
        pro_id = j.split(':')[0]
        total_count = k['total'])
        user[i['uid']][pro_id] += total_count
        pro[pro_id] += total_count
		
#commit星期数量
for index, i in enumerate(mydb['commit'].find()):
    d[datetime.datetime.strptime(i['created_at'].split('T')[0], "%Y-%m-%d").weekday()] += 1
	
#后缀对应的语言
with open('C:\\Users\\isaac\\Downloads\\language_extensions.txt') as f:
    for i in f.readlines():
        yuyan, houzhui = i.strip().split(':')
        for i in houzhui.split(','):
            languages[i] = yuyan
			

#统计开发者数量			
for index, i in enumerate(mydb['user'].find()):
    time = i['created_at'].strip().split('-')
    timestr = '-'.join((time[0], time[1]))
    a[timestr] += 1
	
 j = ''
for index, i in enumerate(sorted(a.keys())):
    if index == 0:
        j = i
        continue
    a[i] += a[j]
    j = i

#祥鑫统计的UserDemo的UserInfo表中有人的skill中的语言得分是0
#出错位置是从commit的前端页面爬取html元素内容的时候
#所以把所有得分是0的都去掉
#按语言排序
a = defaultdict(list)`
for i in mydb['UserInfo'].find():
    for j, k in i['skills']['tag']['pl'].items():
        a[j].append((i['userID'], k))
b = dict()
for i, j in a.items():
    b[i] = dict()
    c = sorted(j, key=lambda x: x[1], reverse=True)
    b[i]['user_id'] = [x[0] for x in c]
    b[i]['score'] = [x[1] for x in c]
		
#按开发者排序
c = defaultdict(lambda: defaultdict(list))
for i in range(1, 129):
    for j, k in b.items():
        if i in k['user_id']:
            index = k['user_id'].index(i)
            c[i]['language'].append(j)
            c[i]['rank'].append(index+1)
            c[i]['score'].append(k['score'][index])
for i, j in c.items():
    temp = sorted([(q,w,e) for q,w,e in zip(j['language'], j['rank'], j['score'])], key = lambda x: (x[1], -x[2]))
    j['language'] = [y[0] for y in temp]
    j['rank'] = [y[1] for y in temp]
    j['score'] = [y[2] for y in temp]