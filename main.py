import requests

wwdc2022_url = "https://developer.apple.com/wwdc22/sessions/"

ret = requests.get(wwdc2022_url)

print(ret.url)
print(ret.text)


def get_all_video_urls():
    return ["a"]

def get_video_download_urls(session_detail_url):
    return ["a"]

def download_file(url):
    print("a")