import time
import re
import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

loginname = "18793175967"
password = "12398qq"
time_delay=0.6
keyword = "东北石油大学超话"
maxWeibo = 10000  # 设置最多多少条微博，如果未达到最大微博数量可以爬取当前已解析的微博数量
weibo_data = []
id = 0
id_list = []
weibo_username_list = []
weibo_userlevel_list = []
weibo_content_list = []
shares_list = []
comments_list = []
likes_list = []
weibo_time_list = []
keyword_list = []
read_num_list = []
post_num_list = []
fans_num_list = []
# 超话主页
keyword_url = "https://m.weibo.cn/p/index?extparam=%E4%B8%9C%E5%8C%97%E7%9F%B3%E6%B2%B9%E5%A4%A7%E5%AD%A6&containerid=10080885b1d2f9945d7e25858b0484e45869b5&luicode=" \
              "10000011&lfid=100103type%3D98%26q%3D%E4%B8%9C%E5%8C%97%E7%9F%B3%E6%B2%B9%E5%A4%A7%E5%AD%A6%E8%B6%85%E8%AF%9D%26t%3D0"


def login(loginname, password):
    browser.get(
        "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F")
    time.sleep(1)

    # 登陆
    elem = browser.find_element_by_xpath("//*[@id='loginName']");
    elem.send_keys(loginname)
    elem = browser.find_element_by_xpath("//*[@id='loginPassword']");
    elem.send_keys(password)
    elem = browser.find_element_by_xpath("//*[@id='loginAction']");
    elem.send_keys(Keys.ENTER)
    time.sleep(15)


def transfer_clicks(browser):
    try:
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
    except:
        pass
    return "Transfer successfully \n"


# 格式化数据
def format_data(shares, comments, likes, weibo_time):
    year = time.strftime('%Y', time.localtime(time.time()))
    mon = time.strftime('%m', time.localtime(time.time()))
    day = time.strftime('%d', time.localtime(time.time()))

    if str(shares).__eq__("转发"):
        shares = 0
    if str(comments).__eq__("评论"):
        comments = 0
    if str(likes).__eq__("赞"):
        likes = 0
    if str(weibo_time).__contains__("小时前"):
        weibo_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    elif str(weibo_time).__contains__("分钟前"):
        weibo_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    elif str(weibo_time).__contains__("刚刚"):
        weibo_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    elif str(weibo_time).__contains__("昨天"):
        weibo_time = str(year) + "-" + str(mon) + str(int(day) - 1)
    elif int(str(weibo_time).split('-')[0]) > 2000:
        weibo_time = weibo_time
    else:
        weibo_time = str(year) + "-" + weibo_time
    return int(shares), int(comments), int(likes), weibo_time


# 封装数据
def packet_data(id, weibo_username, weibo_userlevel, weibo_content, shares, comments, likes,
                weibo_time, keyword, read_num, post_num, fans_num):
    id_list.append(id)
    weibo_username_list.append(weibo_username)
    weibo_userlevel_list.append(weibo_userlevel)
    weibo_content_list.append(weibo_content)
    shares_list.append(shares)
    comments_list.append(comments)
    likes_list.append(likes)
    weibo_time_list.append(weibo_time)
    keyword_list.append(keyword)
    read_num_list.append(read_num)
    post_num_list.append(int(post_num))
    fans_num_list.append(int(fans_num))


# 插入数据
def insert_data(elems):
    global id

    for elem in elems:
        id += 1
        print("正在处理第"+str(elems.index(elem))+"条微博数据")
        # 用户名
        weibo_username = elem.find_elements_by_css_selector('h3.m-text-cut')[0].text
        weibo_userlevel = "普通用户"
        # 微博等级
        try:
            weibo_userlevel_color_class = elem.find_elements_by_css_selector("i.m-icon")[
                0].get_attribute("class").replace("m-icon ", "")
            if weibo_userlevel_color_class == "m-icon-yellowv":
                weibo_userlevel = "黄v"
            if weibo_userlevel_color_class == "m-icon-bluev":
                weibo_userlevel = "蓝v"
            if weibo_userlevel_color_class == "m-icon-goldv-static":
                weibo_userlevel = "金v"
            if weibo_userlevel_color_class == "m-icon-club":
                weibo_userlevel = "微博达人"
        except:
            weibo_userlevel = "普通用户"
        # 微博内容
        weibo_content = elem.find_elements_by_css_selector('div.weibo-text')[0].text
        weibo_content = str(weibo_content).replace(keyword, '')
        comment = re.compile(r'#.*#', re.S)
        comment1 = comment.findall(weibo_content)
        weibo_content= weibo_content.replace(comment1[0], '')
        # 转发
        shares = elem.find_elements_by_css_selector('i.m-font.m-font-forward + h4')[0].text
        # 评论
        comments = elem.find_elements_by_css_selector('i.m-font.m-font-comment + h4')[0].text
        # 点赞
        likes = elem.find_elements_by_css_selector('i.m-icon.m-icon-like + h4')[0].text
        # 发布时间
        weibo_time = elem.find_elements_by_css_selector('span.time')[0].text
        shares, comments, likes, weibo_time = format_data(shares, comments, likes, weibo_time)
        # 暂存到列表
        value = [id, weibo_username, weibo_userlevel, weibo_content, shares, comments, likes,
                 weibo_time, keyword, read_num, post_num, fans_num]
        weibo_data.append(value)
        packet_data(id, weibo_username, weibo_userlevel, weibo_content, shares, comments, likes,
                    weibo_time, keyword, read_num, post_num, fans_num)


# 获取当前页面的数据
def get_current_weibo_data(elems):
    # 开始爬取数据
    before = 0
    after = 0
    n = 0

    while True:
        before = after
        transfer_clicks(browser)
        time.sleep(time_delay)
        elems = browser.find_elements_by_css_selector('div.card.m-panel.card9')
        print("当前获取微博最大数量：%d,n当前的值为：%d" % (len(elems), n))
        after = len(elems)
        if after > before:
            n = 0
        if after == before:
            n = n + 1
            time.sleep(3)
        if n == 5:
            print("达到上限,当前关键词最大微博数为：%d" % after)
            insert_data(elems)
            print("已保存所有微博内容,退出系统!")
            break
        if len(elems) > maxWeibo:
            print("当前微博数已达到%d条" % maxWeibo)
            insert_data(elems)
            print("微博数已达上限,保存%d条,退出系统!" % maxWeibo)
            break



browser = webdriver.Chrome()
browser.set_window_size(452, 790)

# 登录
login(loginname, password)
browser.get(keyword_url)
time.sleep(3)
# 阅读 讨论


title_info = browser.find_element_by_xpath(
    '//*[@id="app"]/div[1]/div[1]/div[1]/div[4]/div/div/div/a/div[2]/h4[1]').text
read_num = str(title_info.split("\u3000")[0]).replace("阅读", '')
post_num = str(title_info.split("\u3000")[1]).replace("帖子", '')
fans_num = str(title_info.split("\u3000")[2]).replace("粉丝", '')

html = browser.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
elems = browser.find_elements_by_css_selector('div.card.m-panel.card9')

get_current_weibo_data(elems)
value_title = ["id", "用户名称", "微博等级", "微博内容", "微博转发量", "微博评论量", "微博点赞",
               "发布时间", "话题名称", "阅读数", "帖子数", "粉丝数"]
end_data = pd.DataFrame({"id": id_list, "用户名称": weibo_username_list, "微博等级": weibo_userlevel_list,
                         "微博内容": weibo_content_list,
                         "微博转发量": shares_list, "微博评论量": comments_list, "微博点赞": likes_list,
                         "发布时间": weibo_time_list, "话题名称": keyword_list, "阅读数": read_num_list,
                         "帖子数": post_num_list, "粉丝数": fans_num_list}, columns=value_title)
end_data.to_excel('weibo1.xls', index=None)
