import httpx
import asyncio
from bs4 import BeautifulSoup


class BaseParser:

    base_url = ''

    async def get_response(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, headers={
                'date': 'Sun, 29 Aug 2021 10:53:02 GMT',
                'content-type': 'text/html; charset=windows-1251', 
                'transfer-encoding': 'chunked', 
                'connection': 'keep-alive', 
                'expires': 'Thu, 01 Jan 1970 00:00:00 GMT', 
                'cache-control': 'no-cache, must-revalidate', 
                'pragma': 'no-cache', 
                'cf-cache-status': 'HIT', 
                'age': '381', 
                'expect-ct': 
                'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"', 
                'vary': 'Accept-Encoding', 
                'server': 'cloudflare', 
                'cf-ray': '68653bb8bcc22d37-KBP', 
                'content-encoding': 'gzip'}
                )
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


async def main():
    paser = PdaParser()
    content = await paser.process_html()
    print(content)

asyncio.run(main())