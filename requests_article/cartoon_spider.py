# coding: utf-8
# @Project_Name :   LibraTest
# @File         :   cartoon_spider.py
# @Author       :   'yangcai'
# @Time         :   2020/7/30 15:37
import os
import re
import time

import requests
from bs4 import BeautifulSoup

from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.115'}


def cartoon(folder_name):
    full_name = os.getcwd()
    folder_name = os.path.join(full_name, '漫画', folder_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    url = 'https://www.dmzj.com/info/benghuaitongrenmanhua.html'
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    url_list = html.xpath('//div[@class="tab-content zj_list_con autoHeight"]/ul/li/a/@href')
    name_list = html.xpath('//div[@class="tab-content zj_list_con autoHeight"]/ul/li/a/@title')
    car_list = []
    for num in range(len(url_list)):
        cartoon_dict = dict()
        cartoon_dict['name'] = name_list[num].replace(' ', '')
        cartoon_dict['url'] = url_list[num].replace(' ', '')
        car_list.append(cartoon_dict)
    download_cartoon(car_list, folder_name)


def download_cartoon(car_list, full_name):
    for car in car_list:
        folder_name = os.path.join(full_name, car['name'])
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        download_header = {
            'Referer': car['url']
        }
        car_response = requests.get(car['url'], headers=headers)
        html = BeautifulSoup(car_response.text, 'lxml')
        script_info = html.script
        pics = re.findall(r'\d{13,14}', str(script_info))
        for j, pic in enumerate(pics):
            if len(pic) == 13:
                pics[j] = pic + '0'
        pics = sorted(pics, key=lambda x: int(x))
        car_hou = re.findall(r'\|(\d{6})\|', str(script_info))[0]
        car_qia = re.findall(r'\|(\d{5})\|', str(script_info))[0]
        for idx, pic in enumerate(pics):
            if pic[-1] == '0':
                car_url = 'https://images.dmzj.com/img/chapterpic/' + car_qia + '/' + car_hou + '/' + pic[:-1] + '.jpg'
            else:
                car_url = 'https://images.dmzj.com/img/chapterpic/' + car_qia + '/' + car_hou + '/' + pic + '.jpg'
            car_response = requests.get(car_url, headers=download_header)
            pic_name = '%03d.jpg' % (idx + 1)
            pic_save_path = os.path.join(folder_name, pic_name)
            with open(pic_save_path, "wb") as file:
                file.write(car_response.content)
        time.sleep(1)


if __name__ == '__main__':
    cartoon_name = '崩坏同人漫画'
    cartoon(cartoon_name)
