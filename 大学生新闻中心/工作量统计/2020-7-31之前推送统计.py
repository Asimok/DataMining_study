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

read_num = []
like_num = []
name = []
title = []
push_time = []
original = []
# 2020-7-31之前推送统计
ab_path = '/Users/asimov/PycharmProjects/DataMining_study/大学生新闻中心/工作量统计/'
start = '2020-03-01'
end = '2020-07-31'
OFFSET = 120
KEY = 'daceb0109d7d5e6811f83a228adffa982dd63a1fb0b331e323030374a3ba2e376845f4cfd6b5c0a0ed1939f00fa639c134ce4372223e5d17ce8df240558b00cf18a1c4d01405a78cb4795ac79ce6fa66e92673f70b20772b0a252e0b876413eb9116ecfafa83ddc160aa4a5d1a55ed36600c0ae3e5f8cdd591922df228ff8302'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/2.4.2(0x12040210) Chrome/39.0.2171.95 Safari/537.36 NetType/WIFI WindowsWechat'
}
articles_url = "http://mp.weixin.qq.com/mp/profile_ext"
yuedu_url = 'https://mp.weixin.qq.com/mp/getappmsgext'
y_param = {}
param = {
    'action': 'getmsg',
    'f': 'json',
    'uin': 'MjMyODkzMzMyMQ==',
    'key': KEY,
    '__biz': 'MzAxMjEzODY0Mw=='
}
data = {
    'is_only_read': '1',
    'appmsg_type': '9'
}

is_bottom = False


def insert_data(all_data):
    # print('插入数据')
    original.append(all_data['is_original'])
    read_num.append(all_data['read_num'])
    like_num.append(all_data['like_num'])
    push_time.append(get_dime(all_data['datetime']))
    title.append(all_data['title'])
    print(all_data['title'])
    name.append(get_name(all_data['text']))


def get_articles_list():
    """
    获取文章列表
    :return: 返回文章列表 list
    """

    articles_json = requests.get(articles_url, params=param, headers=headers, verify=False).json()
    # print(param)
    if 'base_resp' in articles_json.keys():
        print('key值可能失效')
        return None
    return articles_json


def analysis_articles_list():
    """
    解析文章列表参数
    获取除 文章,点赞，在看的所有信息
    :return: 一个字典
    """
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
    if str(content_url).__eq__(''):
        return -1
    cansu = parse.parse_qs(parse.urlparse(content_url).query)
    html_text = requests.get(content_url, headers=headers).text
    html_text = etree.HTML(html_text)
    html_text = html_text.xpath('//div[@id="js_content"]')[0]
    # 判断是否原创
    # articles_info['is_original'] = html_text.xpath('//*[@id="copyright_logo"]/text()')
    is_original = html_text.xpath('//*[@id="copyright_logo"]/text()')
    if len(is_original) > 0:
        articles_info['is_original'] = html_text.xpath('//*[@id="copyright_logo"]/text()')[0]
    else:
        articles_info['is_original'] = ''
    # print(is_original)
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


def get_name(temp_data):
    # 匹配列表
    pattern = ['图文编辑：', '责任编辑：', '原创文字：', '责任编辑：', '摄影记者：', '视频制作：', '图片制作：', '原创图片：']
    exclude = ['\u3000', '\xa0', ' ']
    temp_name = []
    comment = re.compile('(?=图文编辑：).*?(?=责任编辑)', re.S)
    comment1 = comment.findall(temp_data)

    if len(comment1) > 0:
        comment1 = str(comment1[0])
        for i in exclude:
            comment1 = comment1.replace(i, '')

    temp_name.append(comment1)
    # 以提取出推送信息
    # print(temp_name)
    p_name = ''
    if len(temp_name) > 0:
        p_name = str(temp_name[0])
        for i in pattern:
            p_name = p_name.replace(i, ' ' + i)
        print(p_name)
    return p_name


def get_date_interval(now, temp_start):
    # 定义的日期格式需与当前时间格式一致
    # print(date1, date2)

    d1 = datetime.datetime.strptime(now, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(temp_start, '%Y-%m-%d')

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
                    temp_end = get_dime(articles_info['datetime'])
                    # print(articles_info)
                    if get_date_interval(str(temp_end), start) >= 0:
                        print('正在爬取第', i, '篇')
                        i += 1
                        if len(articles_info) > 0:
                            print(temp_end)
                            if get_date_interval(end, str(temp_end)) >= 0:
                                insert_data(articles_info)

                        else:
                            outbreak = True
                            break
                    else:
                        print("已获取 " + str(start) + " 至 " + str(end) + " 推送")
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
    columns = ['日期', '标题', '浏览量', '点赞数', '姓名', '原创']
    info = pd.DataFrame(
        {'标题': title, '浏览量': read_num, '点赞数': like_num, '日期': push_time, '姓名': name, '原创': original},
        columns=columns)
    if os.path.exists(ab_path + start + "-" + end + '  量化统计.xls'):
        info1 = pd.read_excel(ab_path + start + "-" + end + '  量化统计.xls')
        info1 = info1.drop_duplicates().reset_index(drop=True)
        info = pd.concat([info1, info])
        info = info.drop_duplicates().reset_index(drop=True)
    info = info.drop_duplicates().reset_index(drop=True)
    info.to_excel(ab_path + start + "-" + end + '  量化统计.xls', index=None)
    print("------------------------文件已保存------------------------")


if __name__ == "__main__":
    try:
        main()
        write_excel()
    finally:
        print("发生异常")
        write_excel()
    # main()
    # write_excel()
