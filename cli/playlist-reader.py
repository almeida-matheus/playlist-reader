from selenium import webdriver # selenium
from webdriver_manager.chrome import ChromeDriverManager # webdriver_manager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup # beautifulsoup4
import re

class Youtube:

    def __init__(self,link):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('log-level=3') #* hide error logs
        chrome_options.add_argument('--headless') #* don't display the browser
        # service = Service(ChromeDriverManager().install(), options=chrome_options)
        # driver = webdriver.Chrome(service=service)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        driver.get(link)
        content = driver.page_source.encode('utf-8').strip()
        self.soup = BeautifulSoup(content, 'html.parser')

    def get_playlist_name(self):
        pattern_name = re.compile(r'<meta content="(.*?)" name="twitter:title"/>') 
        for match in pattern_name.finditer(self.soup.prettify()):
            name = match.group(1)
        return name.replace(' ','_')

    def get_playlist_tiles(self):
        array_titles = []

        titles = self.soup.find_all("a",attrs={"id": "video-title"})
        for title in titles:
            array_titles.append(title.text.strip())
        return array_titles

    def create_file(self,playlist_name,array_titles):
        file_name = playlist_name + '.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            for line in array_titles:
                f.write(line+'\n')

    def close_driver(self):
        file_name = playlist_name + '.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            for line in array_titles:
                f.write(line+'\n')

if __name__ == '__main__':
    # link = 'https://www.youtube.com/playlist?list=PLMKi-ss_sEoOZw9TB4iCrevTK60uY8wg0'
    link = str(input('❯ enter playlist link: '))

    obj_yt = Youtube(link)

    array_titles = obj_yt.get_playlist_tiles()
    playlist_name = obj_yt.get_playlist_name()
    obj_yt.create_file(playlist_name,array_titles)
    # driver.quit()