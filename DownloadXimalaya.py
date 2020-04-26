import os
import requests
from fake_useragent import UserAgent
from urllib.parse import urlparse


class DownloadXmla(object):
    music_url = ""
    music_name = ""

    def __init__(self, url: str, save_dir: str):
        self.web_url = url
        self.ua = UserAgent()
        self.get_music_name()
        self.get_music_url()
        self.save_dir = save_dir

    def get_music_name(self):
        """
        获取音乐名字
        :return:
        """
        url = "https://www.ximalaya.com/revision/seo/getTdk"
        data = {
            "typeName": "TRACK",
            "uri": urlparse(self.web_url).path
        }
        headers = {"User-Agent": self.ua.random}
        try:
            response = requests.get(url, params=data, headers=headers)
        except Exception as e:
            print(e)
        else:
            self.music_name = response.json()['data']['tdkMeta']['keywords']

    def get_music_url(self):
        """
        获取音乐下载地址
        :return:
        """
        url = "https://www.ximalaya.com/revision/play/v1/audio"
        data = {
            "ptype": 1,
            "id": self.web_url.split('/')[-1]
        }
        headers = {"User-Agent": self.ua.random}
        try:
            response = requests.get(url, params=data, headers=headers)
        except Exception as e:
            print(e)
        else:
            self.music_url = response.json()['data']['src']

    def download(self):
        """
        下载文件的方法
        只是一个简单的写入文件，可以用更多的方法来下载
        :return:
        """
        path = os.path.join(self.save_dir, self.music_name + ".m4a")
        base_dir = os.path.dirname(path)
        # 文件夹不存在创建文件夹
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # 文件存在删除文件
        if os.path.exists(path):
            os.remove(path)
        try:
            response = requests.get(self.music_url)
            with open(path, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(e)


def main():
    xmla = DownloadXmla("https://www.ximalaya.com/youshengshu/21868057/185564327", '.')
    xmla.download()


if __name__ == '__main__':
    main()
