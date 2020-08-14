from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
# url1='https://www.aqistudy.cn/'
url = 'https://movie.douban.com/subject/26266893/comments?start=20&limit=20&sort=new_score&status=P'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
soup.find_all('span')
username = [i.text for i in soup.select('#comments > div > div.comment > h3 > span.comment-info > a')]
star = [i.text for i in soup.select("#comments > div > div.comment > h3 > span.comment-info > span ")]
comment_time = [str(i.text).strip() for i in soup.select("#comments > div > div.comment > h3 > span.comment-info > "
                                                         "span.comment-time")]

print(username)
print(star)
print(comment_time)
