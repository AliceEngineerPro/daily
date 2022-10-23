# coding: utf8
"""
@File: test.py
@Author: Alice(From Chengdu.China)
@HomePage: https://github.com/AliceEngineerPro
@CreatedTime: 2022/10/21 15:57
"""

import requests
import json
from bs4 import BeautifulStoneSoup
from lxml import etree


class MoviesDouban(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        self.proxies = {
            'http': 'http://127.0.0.1:56789',
            'https': 'http://127.0.0.1:56789'
        }
        self.page_number = []
        self.cookies = 'll="118318"; bid=hldy-SvyXH8; ap_v=0,6.0'

    def start_number(self) -> None:
        for number in range(0, 100, 20):
            self.page_number.append(number)

    def get_movies(self) -> None:
        request_url = f'https://m.douban.com/rexxar/api/v2/movie/recommend?'
        for start_number in range(0, 21, 20):
            params = {
                'refresh': '0',
                'start': start_number,
                'count': '20',
                'selected_categories': {},
                'uncollect': False,
                'playable': True,
                'tags': None
            }
            response = requests.request(
                method='GET',
                url=request_url,
                params=params,
                headers=self.headers,
                cookies={cookie.split('=')[0]: cookie.split('=')[1] for cookie in self.cookies.split('; ')},
                proxies=self.proxies,
            )
            print(response.content.decode())

    def get_hot_movies(self) -> list:
        url_list: list = []
        for number in range(0, 351, 50):
            request_url = f'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start={number}'
            response = requests.get(url=request_url, headers=self.headers)
            response_dict = json.loads(response.content.decode())
            for data in response_dict.get('subjects'):
                for data_key, data_value in data.items():
                    if data_key == 'url':
                        url_list.append(data_value)
            #     break
            # break
        return url_list

    @classmethod
    def detailed_hot_movies(cls):
        for url_hot_movie in cls().get_hot_movies():
            detailed_hot_movie_response = requests.request(
                method='GET',
                url=url_hot_movie,
                headers=cls().headers,
            )
            parse_html = etree.HTML(detailed_hot_movie_response.content.decode())
            detailed_hot_movie_name = parse_html.xpath('//span[@property="v:itemreviewed"]/text()')
            detailed_hot_movie_director = parse_html.xpath('//span[@class="attrs"]/a[@rel="v:directedBy"]/text()')
            
            # print(detailed_hot_movie_name, type(detailed_hot_movie_name))
            print(f'电影: {detailed_hot_movie_name[0]} 导演是: {detailed_hot_movie_director[0]}')



