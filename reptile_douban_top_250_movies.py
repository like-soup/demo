from bs4 import BeautifulSoup
import requests
import os
import shutil
import subprocess

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

# 下载图片
# Requests 库封装复杂的接口，提供更人性化的 HTTP 客户端，但不直接提供下载文件的函数。
# 需要通过为请求设置特殊参数 stream 来实现。当 stream 设为 True 时，
# 上述请求只下载HTTP响应头，并保持连接处于打开状态，
# 直到访问 Response.content 属性时才开始下载响应主体内容


def download_jpg(image_url, image_localpath):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(image_localpath, 'wb') as f:
            response.raw.deconde_content = True
            shutil.copyfileobj(response.raw, f)


# 取得海报图片
def get_img_of_movie(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    for pic_href in soup.find_all('div', class_='pic'):
        for pic in pic_href.find_all('img'):
            imgurl = pic.get('src')
            dir = os.path.abspath('.')
            data_path = dir + "/data"
            filename = os.path.basename(imgurl)
            imgpath = os.path.join(data_path, filename)
            print('开始下载 %s' % imgurl)
            download_jpg(imgurl, imgpath)


def get_movies_of_the_page(page):
    page_flag = str(25 * (page - 1))
    url = "https://movie.douban.com/top250?start={}&filter=".format(page_flag)
    print("get the movies of page {}".format(page))
    get_img_of_movie(url)


def delete_date():
    cmd = "pwd"
    subprocess.run(cmd, shell=True)
    delete_cmd = "rm ./data/*.jpg"
    subprocess.run(delete_cmd, shell=True)


if __name__ == '__main__':

    delete_date()
    # 指定查看页数
    for page in range(1, 3):
        get_movies_of_the_page(page)

