# -*- coding: utf-8 -*-
import json
import scrapy
import re
from scrapy.selector import Selector
from  myproject.items import  MyprojectItem
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from  myproject.spiders.DecodeScript import DecodeScript
from myproject.spiders.DecodeFontFile import DecodeFontFile
from scrapy_splash import SplashRequest


class ExamplesItem(scrapy.Item):
    file_urls = scrapy.Field()  # 指定文件下载的连接
    files = scrapy.Field()  # 文件下载完成后会往里面写相关的信息

class autohomeSpider(CrawlSpider):
    name = 'autohomeSpider'
    # 评论的个数
    count = 0
    allowed_domains = ['autohome.com.cn']
    #start_urls = ['https://k.autohome.com.cn/314']
    start_urls = ['http://car.bitauto.com/kaimeirui/koubei/gengduo/1991-0-0-0-0-0-0-0-0-0-0--1-10.html']

    def start_requests(self):  # 重新定义起始爬取点
        for url in self.start_urls:
          yield SplashRequest(url, args={'timeout': 8, 'images': 0},magic_response=True)

    def parse(self, response):
        text = response.xpath('//div[@class="text-con"]')[0]
        span= response.xpath('//div[@class="text-con"]//span')
        s1= span.group().encode('unicode_escape').decode('string_escape')
        #list_span = re.finditer(regex, text)
        #for span in list_span:
        #   tag_span = span.group().encode('unicode_escape').decode('string_escape')
        print(text)

    def parse1(self, response):

        urls = response.css('a.reference.download.internal::attr(href)').extract()
        for url in urls:
            yield ExamplesItem(file_urls=[response.urljoin(url)])
        # 记录个数
        autohomeSpider.count += 1
        print("第：", autohomeSpider.count, "个评论。")
        # print(AutohomeSpider.count)
        # 获取所有评论div //*[@id="maodian"]/div/div/div[2]/div[4]
        divs = response.xpath('//*[@id="maodian"]/div/div/div[2]/div[@class="mouthcon"]')
        mcount=0;
        for div in divs:
            print("----------------------------------")
            item = MyprojectItem()
            # 车ID //*[@id="maodian"]/div/div/div[2]/div[4]/div/div[1]/div[2]/dl[1]/dd/a[1]
            item['CAR_ID'] = div.xpath('div/div[1]/div[2]/dl[1]/dd/a[1]/@href')[0].extract().replace('/', '')
            print(item['CAR_ID'] )
            # 车名字
            item['CAR_NAME'] = div.xpath('div/div[1]/div[2]/dl[1]/dd/a[1]/text()')[0].extract()
            # 用户ID  //*[@id="maodian"]/div/div/div[2]/div[4]/div/div[1]/div[1]/div/div[1]/div[2]/p/a
            USER_ID1 = div.xpath('div/div[1]/div[1]/div/div[1]/div[2]/p/a/@href')[0].extract()
            item['USER_ID'] = re.findall('\d{1,15}', USER_ID1)[0]
            item['USER_NAME'] = div.xpath('div/div[1]/div[1]/div/div[1]/div[2]/p/a/text()')[0].extract().strip()
            # 购买地点 //*[@id="maodian"]/div/div/div[2]/div[4]/   div/div[1]/div[2]/dl[2]/dd
            PURCHASE_PLACE = div.xpath('div/div[1]/div[2]/dl[2]/dd')[0]
            item['PURCHASE_PLACE'] = PURCHASE_PLACE.xpath('string(.)').extract()[0].strip()
            # 因为列表属性相同且数量不确定，所要加入判断
            dls =div.xpath('div/div[1]/div[2]/dl')
            # 正常的有7个
            if dls.__len__() == 7:
                # 购买时间 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[4]/dd
                item['PURCHASE_TIME'] = div.xpath('div/div[1]/div[2]/dl[4]/dd/text()')[0].extract().strip()
                # 裸车购买价 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[5]/dd
                CAR_PRICE = div.xpath('div/div[1]/div[2]/dl[5]/dd')[0]
                item['CAR_PRICE'] = CAR_PRICE.xpath('string(.)').extract()[0].strip().replace('\xa0','')
                # 购车目的 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[7]/dd
                PURCHASE_PURPOSE = div.xpath('div/div[1]/div[2]/dl[7]/dd')[0]
                item['PURCHASE_PURPOSE'] = PURCHASE_PURPOSE.xpath('string(.)').extract()[0].strip().replace('\r\n','').replace('                                ',';')
            #不正常的有6个，分为两种情况：缺经销商和缺油耗。
            elif dls.__len__() == 6:
                p = div.xpath('div/div[1]/div[2]/dl[5]/dt/p')
                # 如果有p标签 ，说明有油耗，没有经销商
                if p:
                    # 购买时间 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[4]/dd
                    item['PURCHASE_TIME'] = div.xpath('div/div[1]/div[2]/dl[3]/dd/text()')[0].extract().strip()
                    # 裸车购买价 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[5]/dd
                    CAR_PRICE = div.xpath('div/div[1]/div[2]/dl[4]/dd')[0]
                    item['CAR_PRICE'] = CAR_PRICE.xpath('string(.)').extract()[0].strip().replace('\xa0', '')
                    # 购车目的 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[7]/dd
                    PURCHASE_PURPOSE = div.xpath('div/div[1]/div[2]/dl[6]/dd')[0]
                    item['PURCHASE_PURPOSE'] = PURCHASE_PURPOSE.xpath('string(.)').extract()[0].strip().replace('\r\n','').replace('                                ', ';')
                # 如果没有p说明 没有油耗，有经销商
                else:
                    # 购买时间 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[4]/dd
                    item['PURCHASE_TIME'] = div.xpath('div/div[1]/div[2]/dl[4]/dd/text()')[0].extract().strip()
                    # 裸车购买价 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[5]/dd
                    CAR_PRICE = div.xpath('div/div[1]/div[2]/dl[5]/dd')[0]
                    item['CAR_PRICE'] = CAR_PRICE.xpath('string(.)').extract()[0].strip().replace('\xa0', '')
                    # 购车目的 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/dl[7]/dd
                    PURCHASE_PURPOSE = div.xpath('div/div[1]/div[2]/dl[6]/dd')[0]
                    item['PURCHASE_PURPOSE'] = PURCHASE_PURPOSE.xpath('string(.)').extract()[0].strip().replace('\r\n','').replace('                                ', ';')
            # 评分- 空间 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/div[1]/dl/dd/span[2]
            item['SCORE_SPACE'] = div.xpath('div/div[1]/div[2]/div[1]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 动力 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/div[2]/dl/dd/span[2]
            item['SCORE_POWER'] = div.xpath('div/div[1]/div[2]/div[2]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 操控
            item['SCORE_CONTROL'] = div.xpath('div/div[1]/div[2]/div[3]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 油耗
            item['SCORE_FUEL_CONSUMPTION'] = div.xpath('div/div[1]/div[2]/div[4]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 舒适性
            item['SCORE_COMFORT'] = div.xpath('div/div[1]/div[2]/div[5]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 外观
            item['SCORE_EXTERIOR'] = div.xpath('div/div[1]/div[2]/div[6]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 内饰
            item['SCORE_INTERIOR'] = div.xpath('div/div[1]/div[2]/div[7]/dl/dd/span[2]/text()')[0].extract()
            # 评分- 性价比 //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[2]/div[8]/dl/dd/span[2]
            item['SCORE_COST_EFFECTIVE'] = div.xpath('div/div[1]/div[2]/div[8]/dl/dd/span[2]/text()')[0].extract()
            #item['SCORE_COST_EFFECTIVE'] = div.xpath('div/div[1]/div[2]/div[8]/dl/dd/span[2]/text()').extract()
            # 评论的url //*[@id="maodian"]/div/div/div[2]/div[4]/ div/div[1]/div[1]/div/div[2]/div[2]
            #url_id_pre = div.xpath('div/div[1]/div[1]/div/div[2]/div[2]/@id')[0].extract()  # 结果为 DivRelatedTopics_1565672
            # url_id_pre = div.xpath('//div[@class="allcont border-b-solid"]/a[1]/@href').extract()
            url_id_pre = div.xpath('//div[@class="allcont border-b-solid"]/a[1]/@href')[mcount].extract()
            # url_id_pre=div.xpath('/div/div[1]/div[2]/div[1]/div[3]/div[1]')[0].extract()
            # 截取id
            #url_id = re.findall('\d{1,20}', url_id_pre)[0]
            # 存入评论url
            item['COMMENT_URL'] = url_id_pre
            # "http://k.autohome.com.cn/FrontAPI/GetFeelingByEvalId?evalId=" + url_id
            COMMENT_URL = 'https:'+item['COMMENT_URL']
            mcount=mcount+1
            print(item)
            yield SplashRequest(url=COMMENT_URL,callback=self.parse_recommand,magic_response=True,args={'timeout': 8,'wait':0.5})
            #  用回调函数获取 评论内容
           #yield SplashRequest(COMMENT_URL, args={'timeout': 8, 'images': 0})
           #yield scrapy.http.Request(url=COMMENT_URL,  meta={'item': item}, callback=self.parse_recommand, dont_filter=True)

    def parse_recommand(self, response):
        print('***********************')
        text = response.body
        #t1= response.css('fonts-face')# response.xpath('//style[@fonts-face]')[0].extract()
        #temp1= response.css('fonts-face').xpath('@src').extract()


        """利用正则获取字体文件链接"""
        regex = r'\w+\..*?ttf'
        font_url=re.findall(regex, response.text)[0]
        decode_fontfile = DecodeFontFile()
        decode_fontfile.download_fontfile(font_url)
        #font_url =txt1[0] #re.findall(regex, text)[0]
        #print(font_url)

        Decode_Script=DecodeScript()
        text=response.xpath('//div[@class="text-con"]')[0].extract()
        print(text)
        list_text = Decode_Script.get_text_con(text,decode_fontfile)
        for text in list_text:
            for key, value in text.items():
                print(key + ":" + value)

if __name__ == '__main__':
    from scrapy import cmdline
    args = "scrapy crawl autohomeSpider".split()
    cmdline.execute(args)




