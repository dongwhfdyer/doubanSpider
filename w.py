import re
import requests
from retrying import retry


class proxies_spider:
    def __init__(self):
        self.url_temp = "https://www.freeip.top/?page={}&protocol=https"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }
        self.ip_lists = []

    def clear_data(self, res):
        mr = re.findall("<td>(.*?)</td>", res)
        # print(mr)
        i = 0
        while True:
            if i >= len(mr):
                break
            self.ip_lists.append(mr[i] + ":" + mr[i + 1])
            i += 11

    @retry(stop_max_attempt_number=3)
    def get_request(self, url):
        print("*" * 25)
        res = requests.get(url, headers=self.headers, timeout=3).content.decode("utf-8")
        return res

    def run(self):
        # urls = "https://www.freeip.top/?page=1&protocol=https"
        # 构造url
        num = 1
        while True:
            url = self.url_temp.format(num)
            try:
                res = self.get_request(url)
            except Exception as e:
                print(e)

            # 清洗数据，把数据存入列表
            self.clear_data(res)
            if len(self.ip_lists) % 15 != 0:
                break
            num += 1

        print(len(self.ip_lists))
        return self.ip_lists

import requests
from DouBan_Sprider import Proxies_spider
from retrying import retry
import json


class Proxies_vertify:
    def __init__(self):
        self.url = "https://www.baidu.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }
        self.end_ip_lists = []

    @retry(stop_max_attempt_number=2)
    def request_get(self, ip):
        requests.get(self.url, headers=self.headers, proxies=ip, timeout=2)

    def run(self):
        # 读取数据，测验是否完整
        proxies_spider = Proxies_spider.proxies_spider()
        ip_list = proxies_spider.run()
        for ip in ip_list:
            try:
                ips = {"https": "https://{}".format(ip)}
                self.request_get(ips)
                self.end_ip_lists.append(ip)
                print("*" * 20)
                print(ip)
            except Exception as e:
                print(e)
        print(self.end_ip_lists)
        with open("Proxies.txt", "a") as f:
            f.write(json.dumps(self.end_ip_lists) + "\n")
        return self.end_ip_lists


import requests
import json
from DouBan_Sprider import Proxies_vertify
from retrying import retry


class DouBan_spider:
    def __init__(self):
        # 初始url
        self.url_list_temp = "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_start={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }

    @retry(stop_max_attempt_number=2)
    def get_request(self, url, proxies):
        res_json = requests.get(url, headers=self.headers, proxies=proxies, timeout=3, verify=False)
        assert res_json.status_code == 200
        return res_json.content.decode("utf-8")

    def write_data(self, res_list):
        with open("douban_sprider.txt", "a", encoding="gbk") as f:
            for data in res_list:
                rate = data["rate"]
                title = data["title"]
                url = data["url"]
                cover = data["cover"]
                f.write("电视剧名称：" + title + ", 影评：" + rate + ", 播放地址：" + url + ", Img_url: " + cover + "\n")

    def run(self):
        # 下一页变量 num+20
        num = 0
        count = 0
        Vertify = Proxies_vertify.Proxies_vertify()
        ip_list = Vertify.run()
        while True:
            url = self.url_list_temp.format(num)
            proxies = {"https": "https://{}".format(ip_list[count])}
            count = (count + 1) % len(ip_list)
            # proxies = {"https": "https://68.183.235.141:8080"}
            try:
                res_json = self.get_request(url, proxies)
                res_list = json.loads(res_json)["subjects"]
                while len(res_list) == 0:
                    break
                # 把数据写入 douban_sprider.txt
                self.write_data(res_list)
                print("第 " + str(int(num / 20) + 1) + "页")
                num += 20
            except Exception as e:
                print(e)


if __name__ == '__main__':
    douban_spider = DouBan_spider()
    douban_spider.run()
