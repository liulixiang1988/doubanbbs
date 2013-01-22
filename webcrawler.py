#!/usr/bin/env python
# -*- coding:utf-8 -*-

from BeautifulSoup import BeautifulSoup as bs
import urllib


def get_page(url):
    return urllib.urlopen(url).read()


def get_content(content):
    head = content.find(name='h4').contents
    reply_datetime = head[0].strip()
    reply_username = head[1].getString()
    reply_userid = head[1].get('href', '')
    reply_content = content.find(name='p')
    return reply_userid, reply_username, reply_datetime, reply_content


def get_all_contents(page):
    '''
    dict_contents = {id: [name. {datetime:content, ...}], ...}
    '''
    soup = bs(page)
    all_contents = soup.findAll(name='div', attrs={'class': 'reply-doc content'})
    dict_contents = {}
    for content in all_contents:
        id, name, time, content = get_content(content)
        if id in dict_contents:
            dict_contents[id][1][time] = content
        else:
            dict_contents[id] = [name, {time:content}]
    return dict_contents


def store_contents(contents):
    try:
        import codecs
        f = codecs.open('result.html', 'w', 'utf-8')
        f.write('<!DOCTYPE html>')
        f.write('<meta charset="utf-8">')
        for id in contents:
            f.write('<h3><a href=%s>%s</a></h3>' % (id, contents[id][0]))
            for r in contents[id][1]:
                f.write('<p class="reply_content"><span class="dt">%s</span><br>%s</p>' % (r, contents[id][1][r]))
        f.close()
        print u'成功保存文件'
    except:
        print u'保存文件失败'


def store_contents2(contents):
    try:
        import codecs
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('./templates'))
        template = env.get_template('contents_list.html')
        result = template.render(contents=contents)
        f = codecs.open('result2.html', 'w', 'utf-8')
        f.write(result)
        f.close()
    except Exception as e:
        print u'保存文件失败\n%s' % e


def main():
    all = get_all_contents(get_page('http://www.douban.com/group/topic/9267121/?start=81300'))
    #store_contents(all)
    store_contents2(all)


if __name__ == '__main__':
    main()
