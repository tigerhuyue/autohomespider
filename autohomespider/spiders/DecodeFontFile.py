# -*- coding:utf-8 -*-

"""解析字体文件"""
from fontTools.ttLib import TTFont
import re
import requests


list_font = [' ', '一', '七', '三', '上', '下', '不', '中', '档', '比', '油', '泥', '灯', '九', '了', '二', '五',
             '低', '保', '光', '八', '公', '六', '养', '内', '冷', '副', '加', '动', '十', '电', '的', '皮', '盘', '真', '着', '路', '身',
             '软', '过', '近', '远', '里', '量', '长', '门', '问', '只', '右', '启', '呢', '味', '和', '响', '四', '地', '坏', '坐', '外',
             '多', '大', '好', '孩', '实', '小', '少', '短', '矮', '硬', '空', '级', '耗', '雨', '音', '高', '左', '开', '当', '很', '得',
             '性', '自', '手', '排', '控', '无', '是', '更', '有', '机', '来']


class DecodeFontFile(object):
    def __init__(self):
        self.file_path = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }

    def download_fontfile(self, font_url):
        font_url = "http://" + font_url
        cont = requests.get(font_url, headers=self.headers).content
        file_name = re.findall(r'\w{20,}[\s\S]*?ttf', font_url)[0]
        self.file_path = "../fonts/" + file_name
        with open(self.file_path, "wb") as f:
           f.write(cont)

    # 创建 self.fonts 属性
    def get_glyph_id(self, glyph):
        ttf = TTFont(self.file_path)
        ttf.saveXML('../fonts/01.xml')
        # gly_list = ttf.getGlyphOrder()  # 获取 GlyphOrder 字段的值
        index = ttf.getGlyphID(glyph)
        # os.remove(self.file_path)
        return index

    def get_font(self, glyph):
        id = self.get_glyph_id(glyph)
        self.parse_font()
        return list_font[id]

    def parse_font(self):
        font1 = TTFont(self.file_path)
        keys, values = [], []
        for k, v in font1.getBestCmap().items():
            if v.startswith('uni'):
                keys.append(eval("u'\\u{:x}".format(k) + "'"))
                values.append(chr(int(v[3:], 16)))
            else:
                keys.append("&#x{:x}".format(k))
                values.append(v)
        print(keys, values)
        return dict(zip(keys, values))





