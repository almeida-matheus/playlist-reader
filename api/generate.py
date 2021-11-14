import re
from bs4 import BeautifulSoup # beautifulsoup4
import requests # requests

HEADER = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

def catch_info(base,pattern,str_add=''):
    '''base text, pattern to search, string to increment if necessary'''
    array = []
    for match in pattern.finditer(base.prettify()):
        array.append(str_add+match.group(1))
    return list(dict.fromkeys(array)) # set(array_video)

def generate(playlist_param):
    try:
        link = 'https://www.youtube.com/playlist?list=' + playlist_param
        response = requests.get(link, headers=HEADER)
        soup = BeautifulSoup(response.text, "html.parser")

        pattern_title = re.compile(r'"title":{"runs":\[{"text":"(.*?)"}\],"accessibility"')
        pattern_img = re.compile(r'{"url":"https:\/\/i(.*?)?sqp=')
        pattern_video = re.compile(r'{"url":"\/watch(.*?)\\')

        array_title = catch_info(soup,pattern_title)
        array_img = catch_info(soup,pattern_img,'https://i')
        array_video = catch_info(soup,pattern_video,'https://www.youtube.com/watch')

        list_array_yt = list(zip(array_title,array_img,array_video))

        response = []
        for i, info in enumerate(list_array_yt):
            response.append({"id": i, "title": info[0], "link_img": info[1], "link_video": info[2]})
        return response

    except Exception as e:
        print(e)
        return False

# response = generate('PLMKi-ss_sEoOZw9TB4iCrevTK60uY8wg0')
# print(response)