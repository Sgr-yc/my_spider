# coding: utf-8
# @Project_Name :   LibraTest
# @File         :   baidu_search_spider.py
# @Author       :   'yangcai'
# @Time         :   2020/7/29 14:44
import os
import re
import time

import requests

url = 'https://www.baidu.com/s?ie=utf-8&wd='
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}


def create_spider(wd_name, pg_count):
    all_url = url + wd_name
    wd_fullname = wd_name + '_链接.txt'
    if os.path.exists(wd_fullname):
        os.remove(wd_fullname)
    all_url_list = []
    for i in range(pg_count):
        all_url = '{0}&pn={1}'.format(all_url, i * 10)
        response = requests.get(all_url, headers=header)
        res_text = response.text.replace('\n', '').replace('\t', '').replace('\r', '')
        res_list = re.findall(r'href =(.*?)target="_blank"(.*?)</a></h3>', res_text)
        for res_t in res_list:
            res_t_url = res_t[0].replace('"', '').replace(' ', '')
            all_url_list.append(res_t_url)
            res_t_name = res_t[1].replace(' ', '').replace('<em>', '').replace('</em>', '').replace('>', '')
            with open(wd_fullname, 'a+', encoding='utf-8') as f:
                f.write('名称：{0}，URL：{1}\n'.format(res_t_name, res_t_url))
        time.sleep(1)


if __name__ == '__main__':
    print('获取百度搜索页链接')
    # 百度搜索的内容
    wd = '博客'
    # 想要获取的总页数
    pn = 10
    create_spider(wd, pn)
    print('获取百度搜索页链接完成')
