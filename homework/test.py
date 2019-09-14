#coding:utf-8

import os
import time
import subprocess
import sys
import json
import matplotlib.pyplot as plt
from collections import defaultdict
sys.path.append('D:\\p3project\\java_api_analyze')
from utils import get_tag_info


def exe_cmd(cm):
    child = subprocess.Popen(cm, shell=True, stdout=subprocess.PIPE)
    return_code = child.poll()
    print(cm)
    while return_code is None:
        time.sleep(1)
        return_code = child.poll()
    line = child.stdout.readlines()
    line = ''.join([x.strip().decode('gbk') for x in line])
    line = line.replace('\\', '/')
    return json.loads(line)


def get_language_from(path):
    a = exe_cmd('C:\\Users\\isaac\\Downloads\\cloc-1.80.exe --json ' + path)
    del a['header']
    del a['SUM']
    return a


def main():
    order = ('wxPython-wxPy-2.8.0.1', 'wxPython-wxPy-2.8.3.0', 'wxPython-wxPy-2.8.6.0', 'wxPython-wxPy-2.8.8.0'
             'wxPython-wxPy-2.8.10.1', 'wxPython-wxPy-2.8.12.0', 'wxPython-wxPy-2.9.2.1', 'wxPython-wxPy-2.9.4.0'
             'wxPython-wxPy-2.9.5.0', 'wxPython-wxPy-3.0.1.0')
    all_lan = dict
    all_lan_set = set()
    path_dir = 'C:\\Users\\isaac\\Desktop\\tmp'
    for index, i in enumerate(os.listdir(path_dir)):
        if i == 'tmp':
            continue
        all_lan[i] = get_language_from(os.path.join(path_dir, i))
    print(all)


def draw():
    names = ('wxPython-wxPy-2.8.0.1', 'wxPython-wxPy-2.8.3.0', 'wxPython-wxPy-2.8.6.0', 'wxPython-wxPy-2.8.8.0',
             'wxPython-wxPy-2.8.10.1', 'wxPython-wxPy-2.8.12.0', 'wxPython-wxPy-2.9.2.1', 'wxPython-wxPy-2.9.4.0',
             'wxPython-wxPy-2.9.5.0', 'wxPython-wxPy-3.0.1.0', 'now')
    x = range(len(names))
    c_cpp = [1699362+163945+119430, 1699362+164162+119434, 1744933+165384+119819, 1758493+165929+119922,
             1816528+166714+119922, 1818592+166857+119922, 2009943+213943+112039, 2030031+214382+112970,
             2053896+224755+135602, 2058318+225563+135985, 1366404+4804+43]
    python = [195475, 199245, 205982, 199716, 194447, 204695, 216838, 218749, 219462, 219484, 402545]
    r = [13756, 13756, 16421, 16421, 16421, 16421, 11078, 11078, 11078, 11078, 15]
    html_xml = [418981+24580, 418981+24603, 418981+24853, 418981+25149, 418981+25267, 418981+25482, 1571+37921,
                1593+38155, 1892+38935, 1892+39858, 10745+197]
    MSBuild_script = [0, 0, 0, 0, 0, 0, 344013, 352508, 196280, 308960, 0]
    plt.plot(x, c_cpp, mec='r', mfc='w', label='c_cpp')
    plt.plot(x, python, ms=10, label='python')
    plt.plot(x, r, ms=10, label='r')
    plt.plot(x, html_xml, ms=10, label='html_xml')
    plt.plot(x, MSBuild_script, ms=10, label='MSBuild_script')
    plt.legend()  # 让图例生效
    plt.xticks(x, names, rotation=45)
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)
    plt.ylabel('code line number')  # X轴标签
    plt.xlabel("version")  # Y轴标签
    plt.title("wxpython")  # 标题

    plt.show()


if __name__ == '__main__':
    draw()