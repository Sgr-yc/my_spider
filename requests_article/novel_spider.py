# coding: utf-8
# @Project_Name :   LibraTest
# @File         :   novel_spider.py
# @Author       :   'yangcai'
# @Time         :   2020/7/30 16:58

import json
import os
import time

import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.115'}


def novel_spider(folder_name):
    full_name = os.getcwd()
    folder_name = os.path.join(full_name, '小说', folder_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    url = 'https://qxs.la/164232/'
    download_header = {
        'Referer': url
    }
    link_response = requests.get(url, headers=headers, timeout=100)
    response_text = link_response.text
    html = etree.HTML(response_text)
    url_list = html.xpath('//div[@class="chapters"]/div[@class="chapter"]/a/@href')
    name_list = html.xpath('//div[@class="chapters"]/div[@class="chapter"]/a/@title')
    for movie_num in range(len(url_list)):
        wd_fullname = os.path.join(folder_name, '{0}.txt'.format(name_list[movie_num].replace(' ', '')))
        novel_url_list = url_list[movie_num].replace(' ', '').split('/')
        novel_url_list = [novel for novel in novel_url_list if novel]
        novel_url = url+novel_url_list[1]+'/'
        novel_response = requests.get(novel_url, headers=download_header, timeout=100)
        novel_response_text = novel_response.text
        html = etree.HTML(novel_response_text)
        content_list = html.xpath('//div[@id="content"]/text()')
        with open(wd_fullname, 'a+', encoding='utf-8') as f:
            for content in content_list:
                f.write(content)
        time.sleep(1)


if __name__ == '__main__':
    novel_spider('完美世界')
