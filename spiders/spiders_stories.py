import logging
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup


def get_stid_and_url_list(pages: int) -> List[Tuple[int, str]]:
    url = 'https://travel.qunar.com/travelbook/list.htm?page={}&order=hot_heat&month=1_2_3'
    ret = []
    for i in range(1, pages + 1):
        response = requests.get(url=url.format(i))
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        all_url = soup.find_all('li', attrs={'class': 'list_item'})
        logging.info('正在爬取第%s页' % i)
        for each in all_url:
            stid = each.find('h2')['data-bookid']
            ret.append((int(stid), 'https://travel.qunar.com/travelbook/note/' + stid))
    return ret


def main():
    for i, (stid, url) in enumerate(get_stid_and_url_list(10)):
        response = requests.get(url=url)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        info = soup.find('p', attrs={'class': 'b_crumb_cont'}).text.strip().replace(' ', '').split('>')

        if len(info) > 2:
            location = info[1].replace('\xa0', '').replace('旅游攻略', '')
            title = info[2].replace('\xa0', '')
        else:
            location = info[0].replace('\xa0', '')
            title = info[1].replace('\xa0', '')
        print('城市：', location)  # 城市
        print('标题：', title)  # 标题

        other_information = soup.find('ul', attrs={'class': 'foreword_list'})

        # 出发日期
        when = other_information.find('li', attrs={'class': 'f_item when'})
        if when is not None:
            time = when.find('p', attrs={'class': 'txt'})
            date = time.find('span', attrs={'class': 'data'}).text.replace(' ', '').strip()
        else:
            date = ""
        print('出发日期：', date)

        # 游玩天数
        howlong = other_information.find('li', attrs={'class': 'f_item howlong'})
        if howlong is not None:
            time = howlong.find('p', attrs={'class': 'txt'})
            day_num = time.find('span', attrs={'class': 'data'}).text.replace(' ', '').strip()
        else:
            day_num = ''
        print('游玩天数：', day_num)

        # 人物
        who = other_information.find('li', attrs={'class': 'f_item who'})
        if who is not None:
            time = who.find('p', attrs={'class': 'txt'})
            relationship = time.find('span', attrs={'class': 'data'}).text.replace(' ', '').strip()
        else:
            relationship = ""
        print('人物：', relationship)

        # 玩法
        how = other_information.find('li', attrs={'class': 'f_item how'})
        if how is not None:
            time = how.find('p', attrs={'class': 'txt'})
            play_ways = time.find('span', attrs={'class': 'data'}).text.replace(' ', '').strip()
        else:
            play_ways = ''
        print('玩法：', play_ways)

        # 人均消费
        how_much = other_information.find('li', attrs={'class': 'f_item howmuch'})
        if how_much is not None:
            time = how_much.find('p', attrs={'class': 'txt'})
            cost = time.find('span', attrs={'class': 'data'}).text.replace(' ', '').strip()
        else:
            cost = ''
        print('平均消费：', cost)

        # 游记作者
        author = soup.find('div', attrs={'class': 'e_line2'}).find('li', attrs={'class': 'head'}).text
        print('作者：', author)

        # 评论数
        comment_num = soup.find('li', attrs={'class': 'nav_item comment'}).find('span', attrs={'class': 'num'}).text
        print('评论数：', comment_num)

        # 点赞量
        likes_num = soup.find('li', attrs={'class': 'nav_item like'}).find('span', attrs={'class': 'num'}).text
        print('点赞数：', likes_num)

        # 浏览量
        views_num = soup.find('span', attrs={'class': 'view_count'}).text.strip()
        print('浏览量：', views_num)

        # 总字数
        passage = soup.find('div', attrs={'id': 'main_box', 'class': 'main_box clrfix'}).text.strip()
        print('总字数', len(passage))

        # 图片数
        image = soup.find('div', attrs={'class': 'b_panel_schedule'}).find_all('img')
        print('图片数', len(image))


if __name__ == '__main__':
    main()
