import httpx
import logging
from bs4 import BeautifulSoup


class BaseParser:

    base_url = ''

    async def get_html_text(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url)
        html = response
        return html.text
    
    async def get_soup(self):
        html = await self.get_html_text()
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

    async def process_html(self):
        soup = await self.get_soup()
        post_headers = soup.find_all('h2',class_='list-post-title')
        content = []
        for post_header in post_headers:
            post = []
            post.append(post_header.get_text())
            post.append(post_header.find('a',href = True)['href'])
            content.append(post)
        return content
