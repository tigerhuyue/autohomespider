# -*- coding: utf-8 -*-
import sys

import json
import os
from fontTools.ttLib import TTFont
import requests
import re


def parse_font():
    font1 = TTFont('fonts\\ChcCQ1sV99GAVa3RAADV0JXwWSA91..ttf')
    keys, values = [], []
    for k, v in font1.getBestCmap().items():
        if v.startswith('uni'):
            keys.append(eval("u'\\u{:x}".format(k) + "'"))
            values.append(chr(int(v[3:], 16)))
        else:
            keys.append("&#x{:x}".format(k))
            values.append(v)
    return keys, values

def download_fontfile(font_url):
        headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }

        font_url = "http://" + font_url
        cont = requests.get(font_url, headers=headers).content
        file_name = re.findall(r'\w{20,}[\s\S]*?ttf', font_url)[0]
        file_path = "../fonts/" + file_name
        with open(file_path, "wb") as f:
            f.write(cont)


if __name__ == '__main__':
    download_fontfile('k2.autoimg.cn/g3/M06/DA/26/ChcCRVsV96KAIGCRAADV7PVTd0489..ttf')
    print("1112222222")


