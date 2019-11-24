# -*- coding: utf-8 -*-
import re
import requests
import time


def crawl_comments_list(page):

    print('let go to page {} in douban.com'.format(int(page)))
    page_flag = str((page - 1) * 20)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    # url = "https://movie.douban.com/subject/1292000/comments?status=P"
    url_page = "https://movie.douban.com/subject/1292000/comments?start={}&limit=20&sort=new_score&status=P".format(page_flag)

    res = requests.get(url_page, headers=headers)
    # 获取每个段子div的正则
    pattern = re.compile("<div class=\"comment-item\" data-cid=.*?<div class=\"comment\">.*?</div>", re.S)

    # print('print res.text...')
    # print(res.text)
    comments = pattern.findall(res.text)
    # for comment in comments:
    #     print(comment)
    # 抽取用户名的正则
    user_pattern = re.compile("<a title=\"(.*?)\" href=", re.S)
    # 抽取评价的正则
    content_pattern = re.compile("<span class=\"short\">(.*?)</span>", re.S)
    print("lets look at comments...")
    for comment in comments:
        user = user_pattern.findall(comment)
        output = []
        if len(user) > 0:
            output.append(user[0])
        content = content_pattern.findall(comment)
        if len(content) > 0:
            output.append(content[0])
        print("\n".join(output))
    print("finish looking at comments on this page!")
    time.sleep(1)


if __name__ == '__main__':

    for page in range(1, 4):
        crawl_comments_list(page)
