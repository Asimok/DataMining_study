import datetime
import html
import json
import os
import re
import time
from urllib import parse

import jieba

jieba.load_userdict('姓名.txt')
import pandas as pd
import requests
from lxml import etree

read_num = []
like_num = []
name = []
title = []
push_time = []
end = '2020-03-01'
OFFSET = 120
headers = {
    # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A403 MicroMessenger/6.5.18 NetType/WIFI Language/zh_CN'
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat'
}

articles_url = "http://mp.weixin.qq.com/mp/profile_ext"
yuedu_url = 'https://mp.weixin.qq.com/mp/getappmsgext'
y_param = {}
param = {
    'action': 'getmsg',
    '__biz': 'MzAxMjEzODY0Mw==',
    'f': 'json',
    'offset': 0,
    'count': 10,
    'scene': 124,
    'uin': 'MjMyODkzMzMyMQ==',
    'key': 'daceb0109d7d5e68c502a136cc5cae0a6ad07c21df3eeb220ab7faa6c343c18a315a5a6e49142394a6d3e4a8a31faeb3cd4eb95fbbd569f6921b6a66d165d45add1314216fa47396026e99a74909f6be',
    'a8scene': 7,
    # 'pass_ticket': '75NyNlpAOE2mOys50t4TZiY+41l96GFJjYFlukUiGU2b4b/7hV05W2n3RIYi3blD',
    # 'appmsg_token': '1070_BiRLn3zNI18G01%2F82v1Lim4JmfEuXGreu4SAqQ~~',
}
data = {
    'is_only_read': '1',
    'appmsg_type': '9'
}

is_bottom = False


def insert_data(all_data):
    # print(all_data)
    read_num.append(all_data['read_num'])
    like_num.append(all_data['like_num'])
    push_time.append(get_dime(all_data['datetime']))
    title.append(all_data['title'])
    print(all_data['title'])
    name.append(get_name(all_data['text']))


def get_articles_list():
    '''
    获取文章列表
    :return: 返回文章列表 list
    '''
    articles_json = requests.get(articles_url, params=param, headers=headers).json()
    print(param)
    if 'base_resp' in articles_json.keys():
        print('key值可能失效')
        return None
    return articles_json


def analysis_articles_list():
    '''
    解析文章列表参数
    获取除 文章,点赞，在看的所有信息
    :return: 一个字典
    '''
    # 获取 10 篇
    articles_json = get_articles_list()
    articles_info = {}
    # 不为空  获取当前文章数 等于0表示没有了
    if articles_json and articles_json.get('msg_count') > 0:
        # 获取文章列表
        articles_lsit = json.loads(articles_json.get('general_msg_list'))
        if articles_lsit.get('list'):
            for articles in articles_lsit.get('list'):
                articles_info['datetime'] = articles.get('comm_msg_info').get('datetime')

                if articles.get('app_msg_ext_info'):
                    articles_info = dict(articles_info, **articles.get('app_msg_ext_info'))
                    articles_info['is_Headlines'] = 1
                    yield articles_info
                    if articles_info.get('is_multi'):
                        for item in articles_info.get('multi_app_msg_item_list'):
                            articles_info = dict(articles_info, **item)
                            articles_info['is_Headlines'] = 0
                            yield articles_info
    else:
        global is_bottom
        is_bottom = True


def get_articles_digset(articles_info):
    time.sleep(1)
    content_url = articles_info.get('content_url').replace('amp;', '')
    # print(content_url)

    content_url = str(content_url).strip()
    if str(content_url).__eq__(''): return -1
    cansu = parse.parse_qs(parse.urlparse(content_url).query)
    html_text = requests.get(content_url, headers=headers).text
    html_text = etree.HTML(html_text)
    html_text = html_text.xpath('//div[@id="js_content"]')[0]
    html_text = etree.tostring(html_text, encoding='utf-8').decode('utf-8')
    dr = re.compile(r'<[^>]+>', re.S)
    wenzhang_text = dr.sub('', str(html_text))
    articles_info['text'] = html.unescape(wenzhang_text).strip()
    y_param['uin'] = param['uin']
    y_param['key'] = param['key']
    data['__biz'] = param['__biz']
    data['mid'] = cansu['mid'][0]
    data['sn'] = cansu['sn'][0]
    data['idx'] = cansu['idx'][0]
    y_json = requests.post(yuedu_url, headers=headers, params=y_param, data=data).json()
    try:
        articles_info['read_num'] = y_json.get('appmsgstat').get('read_num', '0')
        articles_info['like_num'] = y_json.get('appmsgstat').get('like_num', '0')
    except Exception as e:
        articles_info['read_num'] = 0
        articles_info['like_num'] = 0
        print(e)
    return articles_info


def get_name(data):
    # 匹配列表
    pattern = ['图文编辑', '责任编辑', '原创文字', '责任编辑', '摄影记者', '视频制作','图片制作', '原创图片', ':', '：', ' ', ' ']
    temp_name = []
    end_name = ''
    comment = re.compile('(?<=图文编辑：).*?(?=责任编辑)', re.S)
    comment1 = comment.findall(data)
    if len(comment1) > 0:
        p_name = str(comment1[0])
        p_name = ''.join(p_name.split())
        for i in pattern:
            p_name = p_name.replace(i, '')

        p_name = jieba.lcut(p_name)
        for j in p_name:
            end_name = end_name + " " + j
    return end_name


def get_date_interval(now, end):
    # 定义的日期格式需与当前时间格式一致
    # print(date1, date2)

    d1 = datetime.datetime.strptime(now, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(end, '%Y-%m-%d')

    d = (d1 - d2)
    # print('{}  比  {}  晚：{}天'.format(d1, d2, d.days))
    return d.days


def get_dime(timestamp):
    # 利用localtime()函数将时间戳转化成时间数组
    localtime = time.localtime(timestamp)
    dt = time.strftime('%Y-%m-%d', localtime)
    return dt


def main():
    # 主入口
    isbreak = False
    i = 1
    for offset in range(1, 1000):
        # 分页获取文章列表
        if not is_bottom:
            print('正在爬取第%d页' % offset)
            if offset % 2 == 0:
                time.sleep(1)
            param['offset'] = (offset - 1) * 10 + OFFSET

            for articles in analysis_articles_list():
                articles_info = get_articles_digset(articles)
                if articles_info != -1:
                    now = get_dime(articles_info['datetime'])
                    print(now)
                    if get_date_interval(str(now), end) >= 0:
                        print('正在爬取第', i, '篇')
                        i += 1
                        if len(articles_info) > 0:
                            insert_data(articles_info)
                        else:
                            isbreak = True
                            break
                    else:
                        print("已获取" + str(end) + "前推送")
                        print("退出程序")
                        isbreak = True
                        break
            if isbreak:
                break

        else:
            break
        write_excel()
        if isbreak:
            break


def write_excel():
    columns = ['日期', '标题', '浏览量', '点赞数', '姓名']
    info = pd.DataFrame(
        {'标题': title, '浏览量': read_num, '点赞数': like_num, '日期': push_time, '姓名': name},
        columns=columns)
    if os.path.exists('/opt/mq/pytorch_study/东油微博舆情监督/量化统计.xls'):
        info1 = pd.read_excel('量化统计.xls')
        info = pd.concat([info1, info])
        info = info.drop_duplicates().reset_index(drop=True)
    info.to_excel('量化统计.xls', index=None)
    print("文件已保存")


if __name__ == "__main__":
    try:
        main()
    except:
        print("发生异常")
        write_excel()
    write_excel()
