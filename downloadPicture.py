import requests


def download_pic(url):
    request = requests.get(url)

    with open("yzm.png", 'wb') as f:
        f.write(request.content)


download_pic('https://pterclub.com/image.php?action=regimage&imagehash=04c1fdedc030ff34ed50a6a0a1984310')