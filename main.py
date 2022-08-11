import os

import requests
from bs4 import BeautifulSoup
import urllib.request

wwdc2022_url = "https://developer.apple.com/wwdc22/sessions/"
# todo: code
domain_url = "https://developer.apple.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'}


def get_all_video_urls():
    ret = requests.get(wwdc2022_url, headers)
    soup = BeautifulSoup(ret.text, 'html.parser')
    links = soup.find_all(class_="icon icon-after icon-playcircle")
    return list(map(lambda link: domain_url + link.get('href'), links))


def get_video_download_urls(session_detail_url):
    ret = requests.get(session_detail_url, headers)
    soup = BeautifulSoup(ret.text, 'html.parser')
    links = soup.select("li.download > ul > li > a")
    if not links:
        print("no found donwload url at:", session_detail_url)
        return None,None,None

    # hd, sd and other download urls
    hd_video_urls = []
    sk_video_urls = []
    other_urls = []

    for link in links:
        if link.text == "HD Video":
            hd_video_urls.append(link.get("href"))
        elif link.text == "SD Video":
            sk_video_urls.append(link.get("href"))
        else:
            other_urls.append(link.get("href"))

    print("hd", hd_video_urls)
    print("sd", sk_video_urls)
    print("other", other_urls)

    return hd_video_urls, sk_video_urls, other_urls


def download_file(url):
    # fixme: need a nice name
    filename = "test.mp4"
    print("download start.", filename)

    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    print("download end.", filename)


# for url in get_all_video_urls():
#     hd, sd, other = get_video_download_urls(url)
#     if not hd:
#         download_file(hd[0])



url = get_all_video_urls()[0]
hd, sd, other = get_video_download_urls(url)
if hd:
    download_file(sd[0])
