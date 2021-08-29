from os import pardir
import httpx
import asyncio
from bs4 import BeautifulSoup


class BaseParser:

    base_url = ''

    async def get_response(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, headers=headers)
        return response

    
    async def get_soup(self):
        html = await self.get_response()
        if html:
            soup = BeautifulSoup(html.text, 'lxml')
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
        content = ''
        for post_header in post_headers:
            href = post_header.find('a',href = True)['href']
            content += f'{post_header.get_text()}' +'\n' + f'{href}' +'\n'
        return content


class HabrParser(BaseParser):

    def __init__(self) -> None:
        self.base_url = 'https://habr.com/ru/all/'
    
    async def process_html(self):
        soup = await self.get_soup()
        post_headers = soup.find_all('h2',class_='tm-article-snippet__title tm-article-snippet__title_h2')
        content = ''
        for post_header in post_headers:
            href = post_header.find('a',href = True)['href']
            content += f'{post_header.get_text()}' +'\n' + f'{href}' +'\n'
        return content


# async def main():
#     parser = HabrParser()
#     post = await parser.process_html()
#     print(post)

# asyncio.run(main())