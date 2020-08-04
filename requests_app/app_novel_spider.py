import json
import os
import time

import requests


# 爬取笔趣阁app

def novel_spider(folder_name):
    full_name = os.getcwd()
    folder_name = os.path.join(full_name, '小说-APP', folder_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    url = 'https://infosxs.pigqq.com/BookFiles/Html/489/488380/index.html'
    link_response = requests.get(url)
    response_text = link_response.content.decode("utf-8")
    response_dict = json.loads(
        response_text.encode('utf8')[3:].decode('utf8').replace('},]}', '}]}').replace('},]}', '}]}'))
    # print(response_dict['data']['list'])
    for volume in response_dict['data']['list']:
        volume_name = volume['name']
        volume_dir_name = os.path.join(folder_name, volume_name)
        if not os.path.exists(volume_dir_name):
            os.makedirs(volume_dir_name)
        volume_list = volume['list']
        for chapter in volume_list:
            chapter_id = chapter['id']
            url = 'https://contentxs.pigqq.com/BookFiles/Html/489/488380/{0}.html'.format(chapter_id)
            link_response = requests.get(url)
            response_text = link_response.content.decode("utf-8")
            response_dict = json.loads(response_text.encode('utf8')[3:].decode('utf8'))
            # print(response_dict['data']['content'])
            chapter_name = chapter['name']
            wd_fullname = os.path.join(volume_dir_name, '{0}.txt'.format(chapter_name.replace('?', ',')))
            with open(wd_fullname, 'w', encoding='utf-8') as f:
                f.write(response_dict['data']['content'])
            time.sleep(1)


if __name__ == '__main__':
    novel_spider('万界圆梦师')
