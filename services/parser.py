import requests
import logging
from bs4 import BeautifulSoup


class BaseParser:

    base_url = ''

    def get_html_text(self):
        try:
            html = requests.get(self.base_url)
            return html.text
        except requests.exceptions.ConnectionError as e:
            logging.error(f'Error: {e}')
            return 
    
    def get_soup(self):
        html = self.get_html_text()
        if html:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else:
            return
        
    def process_html(self):
        pass

class PdaParser(BaseParser):
    
    def __init__(self):
        self.base_url = "https://4pda.to/"

    def process_html(self):
        soup = self.get_soup()
        post_headers = soup.find_all('h2',class_='list-post-title')
        content = []
        for post_header in post_headers:
            post = []
            post.append(post_header.get_text())
            post.append(post_header.find('a',href = True)['href'])
            content.append(post)
        return content
