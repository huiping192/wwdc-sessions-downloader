import sys
import requests
from bs4 import BeautifulSoup

WWDC_URL = "https://developer.apple.com/videos/wwdc2022/"
DOMAIN_URL = "https://developer.apple.com"

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/14.1.2 Safari/605.1.15'}


def get_all_video_urls(wwdc_sessions_url):
    ret = requests.get(wwdc_sessions_url, REQUEST_HEADERS)
    soup = BeautifulSoup(ret.text, 'html.parser')
    links = soup.find_all(class_="video-image-link")
    return list(map(lambda link: DOMAIN_URL + link.get('href'), links))


def get_video_download_urls(session_detail_url):
    ret = requests.get(session_detail_url, REQUEST_HEADERS)
    soup = BeautifulSoup(ret.text, 'html.parser')
    links = soup.select("li.download > ul > li > a")
    if not links:
        print("no found download url at:", session_detail_url)
        return None, None, None

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
    file_name = "test.mp4"
    print("download start.", file_name)

    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                percent = int(dl * 100 / total_length)
                sys.stdout.write("\r[%s%s]%d%%" % ('=' * done, ' ' * (50 - done), percent))
                sys.stdout.flush()

    print("\n download end.", file_name)


# this is for real!
# for url in get_all_video_urls():
#     hd, sd, other = get_video_download_urls(url)
#     if not hd:
#         download_file(hd[0])

# for test: only download first sd video
url = get_all_video_urls(WWDC_URL)[0]
hd, sd, other = get_video_download_urls(url)
if sd:
    download_file(sd[0])
