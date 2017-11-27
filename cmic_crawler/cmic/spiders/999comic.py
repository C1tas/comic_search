import scrapy
import re
import json
from cmic.items import CmicItem


class Xiaopaiqiu(scrapy.Spider):
    name = "Xiaopaiqiu"
    main_domain = "http://www.999comic.com"
    img_domain = "http://i1.comicgame.top"

    def start_requests(self):
        urls = [
            'http://www.999comic.com/comic/10489/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_url)

    def parse_url(self, response):
        single_hui_list = response.xpath('/html/body/div[6]/div[1]/div[3]/div[3]/ul/li/a')
        faiwai_hui_list = response.xpath('/html/body/div[6]/div[1]/div[3]/div[4]/ul/li/a')
        danxing_hui_list = response.xpath('/html/body/div[6]/div[1]/div[3]/div[5]/ul/li/a')

        # for hui in single_hui_list[127-54+1:]:
        #     hui.xpath('@href')
        # for tmp in single_hui_list[238-54+1:]:
        for tmp in single_hui_list:

            # tmp = single_hui_list[0]
            tmp_url = tmp.xpath('@href').extract()
            goto_img_url = self.main_domain + tmp_url[0]
            # print(goto_img_url)
            yield scrapy.Request(url=goto_img_url, callback=self.parse_img_url)
            # break
            # self.log('ok')

        # tmp = single_hui_list[126-54+1]
        # tmp_url = tmp.xpath('@href').extract()
        # goto_img_url = self.main_domain + tmp_url[0]
        # # print(goto_img_url)
        # yield scrapy.Request(url=goto_img_url, callback=self.parse_img_url)
        # # break
        # self.log('ok')

    def parse_img_url(self, response):
        # print(response.text)
        remove_mark_re = re.compile(r'[\n\r\t]')
        tmp_str = remove_mark_re.sub(" ", response.text)
        filter_content = tmp_str.replace(" ", "")
        img_list_re = re.compile(r'varcInfo=(.*);\$')
        res_img_list = img_list_re.search(filter_content)

        if res_img_list:
            if len(res_img_list.groups()) > 0:
                tmp_json = res_img_list.group(1).replace("'", '"')
                # print(res_img_list.group(1))
                img_list = json.loads(tmp_json)
                # print(img_list)

        # print(img_list)

        re_hui = re.compile(r'([\d]+)')
        if 'ctitle' in img_list:
            print(img_list['ctitle'])
            res_hui_num = re_hui.search(img_list['ctitle'])
            if res_hui_num:
                if len(res_hui_num.groups()) > 0:
                    hui_num = res_hui_num.group(1)

        # print(hui_num)

        if 'fs' in img_list:

            # re_img_order = re.compile(r'([\d]+)\.(?:jpg|gif|png)')
            # print(img_list['fs'])
            for i, tmp in enumerate(img_list['fs']):
                tmp_img_url_list = []
                # tmp = i
                img_url = self.img_domain + tmp
                tmp_img_url_list.append(img_url)

                # res_img_order = re_img_order.search(tmp)
                #
                # if res_img_order:
                #     if len(res_img_order.groups()) > 0:
                #         img_order = res_img_order.group(1)

                new_cimc = CmicItem()
                new_cimc['web_path'] = img_url
                new_cimc['image_urls'] = tmp_img_url_list
                new_cimc['comic_name'] = self.name
                new_cimc['comic_hui'] = int(hui_num)
                new_cimc['img_order'] = int(i)

                yield new_cimc


class Huapai(scrapy.Spider):
    name = "Huapai"
    main_domain = "http://www.999comic.com"
    img_domain = "http://i1.comicgame.top"

    def start_requests(self):
        urls = [
            'http://www.999comic.com/comic/26351/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_url)

    def parse_url(self, response):
        single_hui_list = response.xpath('/html/body/div[6]/div[1]/div[3]/div[3]/ul/li/a')
        faiwai_hui_list = response.xpath('/html/body/div[6]/div[1]/div[3]/div[4]/ul/li/a')
        danxing_hui_list = response.xpath('/html/body/div[6]/div[1]/div[3]/div[5]/ul/li/a')

        # for hui in single_hui_list[127-54+1:]:
        #     hui.xpath('@href')
        # for tmp in single_hui_list[238-54+1:]:
        for tmp in single_hui_list:

            # tmp = single_hui_list[0]
            tmp_url = tmp.xpath('@href').extract()
            goto_img_url = self.main_domain + tmp_url[0]
            # print(goto_img_url)
            yield scrapy.Request(url=goto_img_url, callback=self.parse_img_url)
            # break
            # self.log('ok')

        # tmp = single_hui_list[126-54+1]
        # tmp_url = tmp.xpath('@href').extract()
        # goto_img_url = self.main_domain + tmp_url[0]
        # # print(goto_img_url)
        # yield scrapy.Request(url=goto_img_url, callback=self.parse_img_url)
        # # break
        # self.log('ok')

    def parse_img_url(self, response):
        # print(response.text)
        remove_mark_re = re.compile(r'[\n\r\t]')
        tmp_str = remove_mark_re.sub(" ", response.text)
        filter_content = tmp_str.replace(" ", "")
        img_list_re = re.compile(r'varcInfo=(.*);\$')
        res_img_list = img_list_re.search(filter_content)

        if res_img_list:
            if len(res_img_list.groups()) > 0:
                tmp_json = res_img_list.group(1).replace("'", '"')
                # print(res_img_list.group(1))
                img_list = json.loads(tmp_json)
                # print(img_list)

        # print(img_list)

        re_hui = re.compile(r'([\d]+)')
        if 'ctitle' in img_list:
            print(img_list['ctitle'])
            res_hui_num = re_hui.search(img_list['ctitle'])
            if res_hui_num:
                if len(res_hui_num.groups()) > 0:
                    hui_num = res_hui_num.group(1)

        # print(hui_num)

        if 'fs' in img_list:

            # re_img_order = re.compile(r'([\d]+)\.(?:jpg|gif|png)')
            # print(img_list['fs'])
            for i, tmp in enumerate(img_list['fs']):
                tmp_img_url_list = []
                # tmp = i
                img_url = self.img_domain + tmp
                tmp_img_url_list.append(img_url)

                # res_img_order = re_img_order.search(tmp)
                #
                # if res_img_order:
                #     if len(res_img_order.groups()) > 0:
                #         img_order = res_img_order.group(1)

                new_cimc = CmicItem()
                new_cimc['web_path'] = img_url
                new_cimc['image_urls'] = tmp_img_url_list
                new_cimc['comic_name'] = self.name
                new_cimc['comic_hui'] = int(hui_num)
                new_cimc['img_order'] = int(i)

                yield new_cimc



