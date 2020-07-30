# coding: utf-8
# @Project_Name :   LibraTest
# @File         :   movie_top250_spider.py
# @Author       :   'yangcai'
# @Time         :   2020/7/22 16:13
import json
import os
import time

import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.115'}


def movie_top_spider():
    wd_fullname = '豆瓣电影top250.json'
    if os.path.exists(wd_fullname):
        os.remove(wd_fullname)
    url = 'https://movie.douban.com/top250?start='
    all_url_list = list()
    for i in range(10):
        value_url = '{0}{1}'.format(url, i * 25)
        link_response = requests.get(value_url, headers=headers, timeout=100)
        response_text = link_response.text
        html = etree.HTML(response_text)
        index_list = html.xpath('//ol/li/div/div[1]/em/text()')
        name_list = html.xpath('//ol/li/div/div/div/a/span[1]/text()')
        url_list = html.xpath('//ol/li/div/div/div/a//@href')
        director_list = html.xpath('//ol/li/div/div/div/p[1]/text()')
        score_list = html.xpath('//ol/li/div/div/div/div/span[2]/text()')
        quote_list = html.xpath('//ol/li/div/div/div/p[2]/span/text()')
        for movie_num in range(len(name_list)):
            movie_dict = dict()
            movie_dict['index'] = index_list[movie_num].replace(' ', '')
            movie_dict['name'] = name_list[movie_num].replace(' ', '')
            movie_dict['url'] = url_list[movie_num].replace(' ', '')
            movie_dict['director'] = director_list[movie_num * 2].replace('\n', '').replace(' ', '').replace('\xa0', '')
            movie_dict['type'] = director_list[movie_num * 2 - 1].replace('\n', '').replace(' ', '').replace('\xa0', '')
            movie_dict['score'] = score_list[movie_num].replace(' ', '')
            movie_dict['quote'] = '' if movie_num >= len(quote_list) else quote_list[movie_num].replace(' ', '')
            all_url_list.append(movie_dict)
    with open(wd_fullname, 'a+', encoding='utf-8') as f:
        json.dump(all_url_list, f, ensure_ascii=False, indent=4)
    time.sleep(1)


if __name__ == '__main__':
    movie_top_spider()
