"""
统一IP代理爬虫
"""
import re
import json
from bs4 import BeautifulSoup
import requests

IP_TXT = open('ip.txt', 'a+')


class ProxyPool:
    """
    代理池爬虫类
    """
    session = requests.Session()
    headers = {
        'User-Agent':
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36(KHTML,"
        "like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        'Accept':
        "text/html application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    def __init__(self, url):
        self.url = url

    def start(self):
        """
        开始运行
        """
        dom = self._get_html()
        ip_selectors = self._get_port_selector(dom)
        for ip_selector in ip_selectors:
            port = self._get_port(ip_selector)
            ip_port = ip_selector.text + ':' + port
            if self._test_ip(ip_port):
                IP_TXT.write(ip_port + '\n')
                IP_TXT.flush()
                print('success:', ip_port)

    def _get_html(self):
        """
        获取页面内容
        """
        res = self.session.get(
            self.url,
            headers=self.headers,
            proxies={
                'http': 'http://127.0.0.1:2055'
            })
        dom = BeautifulSoup(res.text, 'lxml')
        return dom

    def _get_port_selector(self, dom):
        """
        获取 ip 所在选择器

        Patameters
        ---------
        dom : 抓取的网页的 dom
        """
        ips = dom.find_all(
            text=re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])'))
        ip_selectors = []
        for ip in ips:
            ip_selector = ip.parent
            ip_selectors.append(ip_selector)
        return ip_selectors

    def _get_port(self, selector):
        """
        获取端口号
        
        Patameters
        ---------
        selector : ip 所在的元素
        """
        while True:
            selector = selector.parent
            port = self._find_port(selector)
            if port:
                break
        return port

    @staticmethod
    def _find_port(selector):
        """
        根据 ip 查找端口号

        Patameters
        ---------
        selector : ip 所在的元素
        """
        port = selector.find(
            text=re.compile(r'^(\s|\'|\"*)\d{2,5}(\s|\'|\")*$'))
        return port

    def _test_ip(self, ip):
        """
        普通代理测试

        Patameters
        ---------
        ip : 需要测试的 ip
        """
        proxies = {'http': 'http://' + ip}
        can = False
        try:
            res = requests.get(
                'http://service.cstnet.cn/ip',
                headers=self.headers,
                proxies=proxies,
                timeout=5)
            bs = BeautifulSoup(res.text, 'lxml')
            test_ip = bs.find(attrs={'class': 'ip-num'})
            if test_ip.text == ip.split(':')[0]:
                can = True
        except:
            print('error:', ip)

        return can

    def test_real_ip(self, ip):
        """
        高匿代理测试

        Patameters
        ---------
        ip : 需要测试的 ip
        """
        proxies = {'http': 'http://' + ip}
        try:
            res = requests.get(
                'https://httpbin.org/ip',
                headers=self.headers,
                proxies=proxies,
                timeout=5)
            res = json.loads(res.text)
            print('success:', res['origin'])
        finally:
            print('error:', ip)


if __name__ == '__main__':
    # 抓取失败的代理网站
    # https://proxy.mimvp.com/free.php
    # http://www.data5u.com/free/index.shtml
    # http://www.goubanjia.com/free/index.shtml

    # 可以抓取的代理网站
    ip_sites = [
        'http://cn-proxy.com/', 'http://www.xicidaili.com/nn/',
        'https://www.kuaidaili.com/free/inha/'
    ]

    for i in ip_sites:
        proxy = ProxyPool('http://cn-proxy.com/')
        proxy.start()

    IP_TXT.close()
