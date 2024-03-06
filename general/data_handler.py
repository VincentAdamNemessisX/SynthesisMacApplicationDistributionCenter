import os
import re
from datetime import datetime


def handle_uploaded_image(file, upload_to):
    path = str("media/" + upload_to + datetime.now().strftime('%Y')
               + "/" + datetime.now().strftime('%m'))
    if not os.path.exists(path):
        os.makedirs(path)
    if file is None:
        return None
    file_name = file.name
    if len(file_name) > 6:
        file_name = file.name[-6:]
    path = (path + "/" +
            str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S-'))
            + file_name)
    with open(path, "wb") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path.replace('media/', '')


def unload_image_from_server(url):
    if os.path.exists('media/' + url):
        os.remove('media/' + url)
    else:
        raise Exception('Image not found')


def get_image_urls_from_md_str(md_str):
    # 定义一个正则表达式，匹配!这样的格式
    pattern = r'!\[\]\((.+?)\)'
    # 使用re.findall函数，返回所有匹配的url
    image_urls = re.findall(pattern, md_str)
    # 打印结果
    if len(image_urls) > 0:
        return image_urls
    else:
        return None
