from bs4 import BeautifulSoup, SoupStrainer
import requests
from pprint import pprint

page = requests.get('https://www.xpertio.net/architekten-goeken-henckel-gbr_oldenburg/10/16145')
soup = BeautifulSoup(page.content, 'html.parser')
with open('./test_html.txt', 'w', encoding='utf8') as file:
    file.write(str(soup.prettify()))