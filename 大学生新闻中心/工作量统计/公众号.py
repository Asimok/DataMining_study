import datetime
import html
import json
import os
import re
import time
from urllib import parse
import pandas as pd
import requests
from lxml import etree
import jieba


jieba.load_userdict('姓名.txt')

read_num = []
like_num = []
name = []
title = []
push_time = []
start = '2020-03-01'
end = '2020-07-31'
OFFSET = 120
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/2.4.2(0x12040210) Chrome/39.0.2171.95 Safari/537.36 NetType/WIFI WindowsWechat'
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
    'key': '89e0d01dbcbac2dcf8363305d452b9dce1246a241f1cbb44668f570c3f77ec90ea9f1dfb3591da5627a2054935040c91520429c5e52a411e96212d64a8ea0a3b5b6049d65b6e0021baa5ba2aef75d0918edc1499a4353a732905adcda07749e891becd4c54e506d1d5560050570ecd5e6b26e1bc99b20eb67f3344bb9055db09',
    'a8scene': 7,

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

    articles_json = requests.get(articles_url, params=param, headers=headers, verify=False).json()
    # print(param)
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
        articles_list = json.loads(articles_json.get('general_msg_list'))
        if articles_list.get('list'):
            for articles in articles_list.get('list'):
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
    pattern = ['图文编辑', '责任编辑', '原创文字', '责任编辑', '摄影记者', '视频制作', '图片制作', '原创图片', ':', '：', ' ', ' ']
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


def get_date_interval(now, start):
    # 定义的日期格式需与当前时间格式一致
    # print(date1, date2)

    d1 = datetime.datetime.strptime(now, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(start, '%Y-%m-%d')

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
    outbreak = False
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
                    # 截止时间
                    # end = get_dime(articles_info['datetime'])
                    #
                    # print(end)
                    if get_date_interval(str(end), start) >= 0:
                        print('正在爬取第', i, '篇')
                        i += 1
                        if len(articles_info) > 0:
                            insert_data(articles_info)
                        else:
                            outbreak = True
                            break
                    else:
                        print("已获取 " + str(start) + " 至 "+str(end)+" 推送")
                        print("退出程序")
                        outbreak = True
                        break
            if outbreak:
                break

        else:
            break
        write_excel()
        if outbreak:
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
