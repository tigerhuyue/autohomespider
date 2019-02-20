# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import re
from myproject.spiders.DecodeFontFile import DecodeFontFile

class DecodeScript(object):

    def get_list_part(self, text_con):
        """传入口碑内容,返回拆分后的列表"""
        return str(text_con).split('【')[1:]
    def get_list_title_con_js(self, part_con):
        """获取标题和混淆的js代码"""
        # 获取小标题
        title = part_con.split("】")[0]
        # 获取加密的文本
        start = re.search('<!--@athm_BASE64@-->', part_con).span()[1]
        end = re.search('<!--@athm_js@-->', part_con).span()[0]
        part_base64 = part_con[start: end]
        # 获取混淆的js代码
        soup_part = BeautifulSoup(part_con, "lxml")
        h_js = soup_part.find('script')
        # 将标题和混淆的js存入一个列表
        list_title_con_js = [title, part_base64, h_js]
        return list_title_con_js

    def put_js(self, js):
        """组装js代码"""

        # 去掉多余字符,用切片也可以
        # if '<script>' in js:
        #     js = js.replace('<script>', "")
        # if '</script>' in js:
        #     js = js.replace('</script>', "")
        js = str(js)[8:-9]
        # 在开始处定义变量
        def_var = "var result = "
        js = def_var + js
        # 在指定位置定义数组
        first_point = js.index("{")
        def_arr = "var arr = [];"
        js = js[:first_point + 1] + def_arr + js[first_point + 1:]
        # 在指定位置给数组赋值
        regex = r"function\s*\w+\(\)\s*\{\s*(\w+)\s*=[\s\S]*?\);\s*(\w+)\s*=[\s\S]*?\);\s*(\w+)\s*=[\s\S]*?\);"
        tuple_groups = re.search(regex, js).groups()
        second_point = re.search(regex, js).span()[1]
        set_arr = "arr = [" + str(tuple_groups[0]) + ", " + str(tuple_groups[1]) + "];"
        js = js[:second_point] + set_arr + js[second_point:]
        # 在指定位置return数组
        add_return = "return arr;"
        js = js.strip()
        js = js[:-13] + add_return + js[-13:]
        return js

    def run_js(self, js):
        """在v8中运行js,获得16进制数字和对应数字"""
        list_num16 = []
        list_index = []
        #default=execjs.get().name
        #ctx =execjs.compile(js)
        # 删除一些无关的字符
        # jscode = js.replace('document.write(s);', '').replace(', true);', ')').replace('var s =', '')
        # 执行代码
        #return ctx.eval(js)
        print("-------------------")


    def replace_span(self, part_con, decode_fontfile):
        """用16进制数字替换掉段落中的span"""
        list_title_con_js = self.get_list_title_con_js(part_con)
        title = list_title_con_js[0]  # 获取标题
        con = list_title_con_js[1]  # 获取加密后段落
        #js = self.put_js(list_title_con_js[2])  # 获取js后重新组装
        #list_num16_index = self.run_js(js)  # 利用v8运行js,获得16进制数字和对应关系
        #list_num16 = list_num16_index[0]
        #list_num16 = list_num16[0].split(",")
        #list_index = list_num16_index[1]
        regex = r"<span\s*style[\s\S]*?font-family:myfont[\s\S]*?</span>"
        list_span = re.finditer(regex, con)
        for span in list_span:
            tag_span = span.group().encode('unicode_escape').decode()
            s = tag_span.find('u')
            e = tag_span.find('</')
            num16 = tag_span[s + 1:e]
            glyph = "uni" + num16.upper()

            font = decode_fontfile.get_font(glyph)
            con = con.replace(tag_span, font)
        return {title: str(con)}

    def get_text_con(self, text_con,decode_fontfile):

        # 传入完成口碑加密内容, 返回按标题分割的片断列表
        list_part = self.get_list_part(text_con)
        content = []
        for part_con in list_part:
            part_text = self.replace_span(part_con, decode_fontfile)
            content.append(part_text)
        return content


