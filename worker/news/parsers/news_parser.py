import sys
sys.path.append('../../')

import base.base_parser as base_parser
import news.parsers.base_parser as self_base_parser
import init
import utils.tools as tools
from utils.log import log
import base.constance as Constance
from extractor.article_extractor import ArticleExtractor
# print(article_extractor.article_extractor)
# 必须定义 网站id
SITE_ID = 1
# 必须定义 网站名
NAME = '新闻正文提取'

DEPTH = int(tools.get_conf_value('config.conf', "collector", "depth"))

# 必须定义 添加网站信息
@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')
    pass

# 必须定义 添加根url
@tools.run_safe_model(__name__)
def add_root_url(parser_params = {}):
    log.debug('''
        添加根url
        parser_params : %s
        '''%str(parser_params))

    for task in parser_params:
        website_id = task[0]
        website_name = task[1]
        website_position = task[2]
        website_url = task[3]
        website_domain = tools.get_domain(website_url)

        base_parser.add_url('news_urls', SITE_ID, website_url, remark = {'website_name':website_name, 'website_position':website_position, 'website_url':website_url, 'website_domain':website_domain})

# 必须定义 解析网址
def parser(url_info):
    url_info['_id'] = str(url_info['_id'])
    log.debug('处理 \n' + tools.dumps_json(url_info))

    root_url = url_info['url']
    depth = url_info['depth']
    site_id = url_info['site_id']
    remark = url_info['remark']
    website_name = remark['website_name']
    website_position = remark['website_position']
    website_url = remark['website_url']
    website_domain =  remark['website_domain']

    html = tools.get_html(root_url)
    if not html:
        base_parser.update_url('news_urls', root_url, Constance.EXCEPTION)
        return

    # 近一步取待做url
    if depth < DEPTH:
        urls = tools.get_urls(html)
        for url in urls:
            url = tools.get_full_url(website_url, url)
            if website_name == '百度新闻':
                remark['website_name'] = ''
                remark['website_domain'] = tools.get_domain(url)
                remark['website_position'] = None
                base_parser.add_url('news_urls', SITE_ID, url, depth + 1, remark = remark)
            elif website_domain in url:
                base_parser.add_url('news_urls', SITE_ID, url, depth + 1, remark = remark)

    # 解析网页
    content = title = release_time = author = ''
    article_extractor = ArticleExtractor(root_url, html)
    content = article_extractor.get_content()
    if content:
        title = article_extractor.get_title()
        release_time = article_extractor.get_release_time()
        author = article_extractor.get_author()
        uuid = tools.get_uuid(title, website_domain) if title != website_name else tools.get_uuid(root_url, ' ')

        log.debug('''
            uuid         %s
            title        %s
            author       %s
            release_time %s
            website_name %s
            domain       %s
            position     %s
            url          %s
            content      %s
            '''%(uuid, title, author, release_time, website_name, website_domain, website_position, root_url, content))

        if tools.is_have_chinese(content):
            # 入库
            self_base_parser.add_news_acticle(uuid, title, author, release_time, website_name, website_domain, website_position, root_url, content)

    log.debug('%s 处理完成'%root_url)
    base_parser.update_url('news_urls', root_url, Constance.DONE)

if __name__ == '__main__':
    url_info = {'url': 'http://shuhua.dzwww.com/tplb/201801/t20180103_16864324.htm', 'status': 0, 'remark': {'website_domain': None, 'website_url': 'http://www.dzwww.com/', 'website_position': 15, 'website_name': '山东大众网'}, '_id': '5a5ea26ecdd76b52e8bb745d', 'site_id': 1, 'retry_times': 0, 'depth': 1}
    parser(url_info)
