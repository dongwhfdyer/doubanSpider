import  urllib
import json
import re
import requests
from bs4 import BeautifulSoup

def crawl_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64'
    }
    url = 'https://movie.douban.com/subject/1433330/reviews'+url
    # url = 'https://movie.douban.com/subject/30482003/reviews'+url
    print(url)
    cookies_str ='bid=mb86bNUFbr4; ll="118182"; _vwo_uuid_v2=DEE0A7C5DACC40B8182987117A61B773D|301a0d8b1b603262a13b81ededf6deda; gr_user_id=381b74ef-773e-48a1-a3df-ca7a270d5c0d; douban-fav-remind=1; viewed="26827295_25945179"; __utmz=30149280.1625626904.9.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=30149280; ct=y; __utma=30149280.96659978.1613013981.1625637517.1625642437.13; _pk_ses.100001.8cb4=*; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1625642514%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14971; __utmt=1; _pk_id.100001.8cb4=c2bac1ff1b0b531e.1614935246.8.1625643924.1625640476.; __utmb=30149280.13.10.1625642437; dbcl2="149718929:VKdtAJOCgCA"'
    cookies_dir = {cookie.split('=')[0]:cookie.split('=')[-1] for cookie in cookies_str.split('; ')}
    # try:
    response = requests.get(url, headers=headers,cookies=cookies_dir) #发送请求返回页面数据
    print(response)
    parse(response) #调用parse函数对爬取的页面数据进行解析，并保存为JSON文件

    # except Exception as e:
    #     print(e)

#对爬取的页面数据进行解析，并保存为JSON文件
def parse(response):
    item = {}
    # 将一段文档传入BeautifulSoup的构造方法,就能得到一个文档的对象, 可以传入一段字符串
    soup = BeautifulSoup(response.text, 'lxml')

    # 返回的是class为main review-item的<div>所有标签
    review_list = soup.find_all('div', {'class': 'main review-item'})

    for review_div in review_list:
        # 作者
        author = review_div.find('a', {'class': 'name'}).text
        # 发布时间
        pub_time = review_div.find('span', {'class': 'main-meta'}).text
        # 评分
        rating = review_div.find('span', {'class': 'main-title-rating'})
        if rating:
            rating = rating.get('title')
        else:
            rating = ""
        # 标题
        title = review_div.find('div', {'class': 'main-bd'}).find('a').text
        # 是否有展开按钮
        is_unfold = review_div.find('a', {'class': 'unfold'})
        if is_unfold:
            # 获取评论id
            review_id = review_div.find('div', {'class': 'review-short'}).get('data-rid')
            # 获取内容
            content = get_fold_content(review_id)
        else:
            content = review_div.find('div', {'class': 'short-content'}).text
        if content:
            content = re.sub(r"\s", '', content)

        item = {
            "author":author,
            "pub_time":pub_time,
            "rating":rating,
            "title":title,
            "content":content
        }

        fp.write(json.dumps(item) + "\n")
    # 如果有下一页
    next_url = soup.find('span', {'class': 'next'}).find('a')
    if next_url:
        # 请求下一页的数据
        crawl_data(next_url.get('href'))
    else:
        return
    return

def get_fold_content(review_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    url = "https://movie.douban.com/j/review/{}/full".format(review_id)
    resp = requests.get(url,headers=headers)
    data = resp.json()
    content = data['html']
    content = re.sub(r"(<.+?>)","",content)
    return content
def login(username, password):
    url = 'https://accounts.douban.com/j/mobile/login/basic'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
        'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
        'Origin': 'https://accounts.douban.com',
        'content-Type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'connection': 'keep-alive',
        'Host': 'accounts.douban.com',
        'cookie':'bid=mb86bNUFbr4; ll="118182"; _vwo_uuid_v2=DEE0A7C5DACC40B8182987117A61B773D|301a0d8b1b603262a13b81ededf6deda; gr_user_id=381b74ef-773e-48a1-a3df-ca7a270d5c0d; douban-fav-remind=1; viewed="26827295_25945179"; apiKey=; __utmz=30149280.1625626904.9.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=30149280; ct=y; __utma=30149280.96659978.1613013981.1625637517.1625642437.13; last_login_way=account; ap_v=0,6.0; push_doumail_num=0; push_noty_num=0; __utmv=30149280.14971; __utmt=1; login_start_time=1625643924939; __utmb=30149280.13.10.1625642437',
    }
    # 登陆需要携带的参数
    data = {
        'ck' : '',
        'name': '',
        'password': '',
        'remember': 'false',
        'ticket': ''
    }
    data['name'] = username
    data['password'] = password
    data = urllib.parse.urlencode(data)
    print(data)
    req = requests.post(url, headers=header, data=data, verify=False)

    cookies = requests.utils.dict_from_cookiejar(req.cookies)
    print(cookies)
    return cookies

def get_ip():
    proxy='http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=364661951061462aa75f4e0c005d8a74&orderno=YZ2021770131nTirVI&returnType=2&count=20'





# login('whfyder@163.com','666douban.')
url='https://movie.douban.com/subject/30482003/reviews?sort=time&start=0'

if __name__=='__main__':
    fp = open("reviews.json", 'w', encoding='utf-8')
    # cookies=login('whfdyer@163.com','666douban.')
    # cookies='bid=mb86bNUFbr4; ll="118182"; _vwo_uuid_v2=DEE0A7C5DACC40B8182987117A61B773D|301a0d8b1b603262a13b81ededf6deda; gr_user_id=381b74ef-773e-48a1-a3df-ca7a270d5c0d; douban-fav-remind=1; _vwo_uuid_v2=DEE0A7C5DACC40B8182987117A61B773D|301a0d8b1b603262a13b81ededf6deda; viewed="26827295_25945179"; __utmc=30149280; __utmz=30149280.1625626904.9.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=223695111; __utmz=223695111.1625637524.7.7.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; ct=y; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1625642437%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fq%3D%25E5%259B%25B0%25E5%259C%25A8%25E6%2597%25B6%25E9%2597%25B4%25E9%2587%258C%25E7%259A%2584%25E7%2588%25B6%25E4%25BA%25B2%2B%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.96659978.1613013981.1625637517.1625642437.13; __utma=223695111.179726324.1613013981.1625637524.1625642437.8; __utmb=223695111.0.10.1625642437; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; __utmt=1; __utmv=30149280.14971; dbcl2="149718929:w7sfH5Wd5oo"; ck=-nxF; __utmb=30149280.10.10.1625642437; _pk_id.100001.4cf6=14c07e69d91487b8.1613013981.7.1625642721.1625640479.'
    cookies_str = 'bid=mb86bNUFbr4; ll="118182"; _vwo_uuid_v2=DEE0A7C5DACC40B8182987117A61B773D|301a0d8b1b603262a13b81ededf6deda; gr_user_id=381b74ef-773e-48a1-a3df-ca7a270d5c0d; douban-fav-remind=1; viewed="26827295_25945179"; __utmz=30149280.1625626904.9.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=30149280; ct=y; __utma=30149280.96659978.1613013981.1625637517.1625642437.13; _pk_ses.100001.8cb4=*; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1625642514%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14971; __utmt=1; _pk_id.100001.8cb4=c2bac1ff1b0b531e.1614935246.8.1625643924.1625640476.; __utmb=30149280.13.10.1625642437; dbcl2="149718929:VKdtAJOCgCA"'
    cookies_dir = {cookie.split('=')[0]: cookie.split('=')[-1] for cookie in cookies_str.split('; ')}
    start_url = '?sort=time&start=0'
    print("爬虫执行中，请勿做其他操作，爬取完成后会有提示！目录下会生成reviews.json文件")
    crawl_data(start_url)   #调用前面定义的 crawl_data函数
    fp.close()
    print("爬取完成")