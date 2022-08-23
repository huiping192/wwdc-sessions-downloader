import os.path
import sys
import requests
from bs4 import BeautifulSoup
import argparse
from multiprocessing import Pool

DOMAIN_URL = "https://developer.apple.com"

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/14.1.2 Safari/605.1.15'}

ap = argparse.ArgumentParser()
ap.add_argument('--year', required=True, help='Determine which year of wwdc')
ap.add_argument('--path', required=False, help='Video save path.default is current.')
ap.add_argument('--quality', required=False, help='Video quality support HD and SD. Default is SD.', default="SD")
ap.add_argument('--queue_count', required=False, help='Video download queue count. Default is 3', type=int,
                default=3)
ap.add_argument('--pdf', help='Should download pdf if exists.', action='store_true')

args = vars(ap.parse_args())
wwdc_year = args['year']
save_path = args['path']
video_quality = args['quality']
queue_count = args['queue_count']
need_pdf = args['pdf']


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

    # hd, sd download url
    hd_video_url, sk_video_url, pdf_url = None, None, None

    for link in links:
        if link.text == "HD Video":
            hd_video_url = link.get("href")
        elif link.text == "SD Video":
            sk_video_url = link.get("href")

    pdf_links = soup.select("li.download > a")
    for link in pdf_links:
        if link.text == "Presentation Slides (PDF)":
            pdf_url = link.get("href")
            break

    print("hd", hd_video_url)
    print("sd", sk_video_url)
    print("pdf", pdf_url)

    return hd_video_url, sk_video_url, pdf_url


def download_file(file_url):
    # fixme: need a nice name
    file_name = os.path.basename(file_url).split("?")[0]
    year = format_wwdc_year(wwdc_year)
    file_dic = save_path + year + "/" if save_path is not None else year + "/"
    file_path = file_dic + file_name

    if os.path.exists(file_path):
        print("file exists. skip download~")
        return
    if not os.path.exists(file_dic):
        os.makedirs(file_dic, exist_ok=True)

    print(f"download start. {file_name}")

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


def download_video(session_url):
    hd_video, sd_video, pdf = get_video_download_urls(session_url)
    if hd_video is not None and video_quality.upper() == "HD":
        download_file(hd_video)
    elif sd_video is not None and video_quality.upper() == "SD":
        download_file(sd_video)
    else:
        print(f"No found match {video_quality} video! ")

    if pdf is not None and need_pdf:
        download_file(pdf)


def download_all_sessions():
    session_urls = get_all_video_urls(get_wwdc_url(wwdc_year))
    with Pool(processes=queue_count) as pool:
        pool.map(download_video, session_urls)


if __name__ == "__main__":
    download_all_sessions()
