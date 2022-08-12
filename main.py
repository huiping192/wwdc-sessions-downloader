import os.path
import sys
import requests
from bs4 import BeautifulSoup
import argparse

DOMAIN_URL = "https://developer.apple.com"

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/14.1.2 Safari/605.1.15'}

ap = argparse.ArgumentParser()
ap.add_argument('--year', required=True, help='which year of wwdc')
ap.add_argument('--path', required=False, help='video save path.default is current.')
ap.add_argument('--quality', required=False, help='video quality support HD and SD.default is SD.', default="SD")

args = vars(ap.parse_args())
wwdc_year = args['year']
save_path = args['path']
video_quality = args['quality']


def format_wwdc_year(wwdc_year):
    return f"wwdc{wwdc_year}"


def get_wwdc_url(wwdc_year):
    year = format_wwdc_year(wwdc_year)
    return f"https://developer.apple.com/videos/{year}/"


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


def download_file(file_url):
    # fixme: need a nice name
    file_name = os.path.basename(file_url).split("?")[0]

    if os.path.exists(file_name):
        print("file exists. skip download~")
        return

    print(f"download start. {file_name}")

    file_path = save_path + file_name if not save_path is None else file_name
    with open(file_path, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(file_url, stream=True)
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


def download_videos(video_urls):
    for url in video_urls:
        download_file(url)


def download_all_sessions():
    for wwdc_url in get_all_video_urls(get_wwdc_url(wwdc_year)):
        hd_videos, sd_videos, other_urls = get_video_download_urls(wwdc_url)
        if hd_videos is not None and video_quality.upper() == "HD":
            download_videos(hd_videos)
        elif sd_videos is not None and video_quality.upper() == "SD":
            download_videos(sd_videos)
        else:
            print(f"No found match video quality {video_quality}! ")


download_all_sessions()

# for test: only download first sd video
# url = get_all_video_urls(get_wwdc_url(wwdc_year))[0]
# hd, sd, other = get_video_download_urls(url)
# if sd:
#     download_file(sd[0])
