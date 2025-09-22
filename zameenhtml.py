from bs4 import BeautifulSoup
import requests

base_url = 'https://www.zameen.com/Homes/Islamabad-3-1.html'

r = requests.get(base_url)
soup = BeautifulSoup(r.text,'html.parser')

with open('zameen_data.html','w',encoding='utf-8') as f:
    for i in range(1,3):
        next_page = f'https://www.zameen.com/Homes/Islamabad-3-{i}.html'
        f.write(soup.prettify())