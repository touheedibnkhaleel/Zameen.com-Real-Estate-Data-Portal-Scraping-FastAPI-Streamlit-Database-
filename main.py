from bs4 import BeautifulSoup
import pandas as pd
import requests
import psycopg2

# file_path = 'zameen_data.html'
# with open(file_path,'r',encoding='utf-8') as fp:
#     soup = BeautifulSoup(fp,'html.parser')
#     container_div = soup.find_all('div', class_="_2a2e3d21")

#     for item in container_div:
#         containers = item.find('a',href=True)
#         if containers:
#             zameen_url = "https://www.zameen.com" + containers['href']
#             urls.add(zameen_url)

conn = psycopg2.connect(database='zameen_property_details',
                        user='postgres', password='blue', port=5432)
cursor = conn.cursor()
urls = set()

page = 1
max_page = 50
while page <= max_page:
    based_url = f"https://www.zameen.com/Homes/Islamabad-3-{page}.html"
    print(f"Scraping listing page: {based_url}") 
    r = requests.get(based_url, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(r.text,'html.parser')
    container_div = soup.find_all('div', class_="_2a2e3d21")

    for item in container_div:
        a_tag = item.find('a', href=True)
        if a_tag:
            href = a_tag['href']
            if href.startswith("/Property/"):
                zameen_url = "https://www.zameen.com" + href
                urls.add(zameen_url)
    page += 1

print(f"Total unique property URLs collected: {len(urls)}")
    
all_data = []

for url in urls:
    fetch_url = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(fetch_url.text,'html.parser')
    titles = soup.find_all('h1',class_='aea614fd')
    details_box = soup.find("ul", class_="_3dc8d08d")

    title = None
    property_type = None
    price = None
    area = None
    purpose = None
    location = None
    bedrooms = None
    bathrooms = None
    added = None

    for i in titles:
        title = i.text

    if details_box:
        for li in details_box.find_all("li"):
            spans = li.find_all("span")
            if len(spans) >= 2:
                label = spans[0].get_text(strip=True)
                value = spans[1].get_text(strip=True)

                if "Type" in label:
                    property_type = value
                elif "Price" in label:
                    price = value
                elif "Area" in label:
                    area = value
                elif "Purpose" in label:
                    purpose = value
                elif "Location" in label:
                    location = value
                elif "Bedroom" in label:
                    bedrooms = value
                elif "Bath" in label:
                    bathrooms = value
                elif "Added" in label:
                    added = value

    print("Scraped:", title, price, area, location) 

    query = """
    INSERT INTO property_details 
    (title,property_type,price,area,purpose,location,bedrooms,bathrooms,added) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """
    data = (title,property_type,price,area,purpose,location,
            None if bedrooms == '-' else bedrooms,
            None if bathrooms == '-' else bathrooms,
            added)

    cursor.execute(query, data)
    conn.commit() 

#     all_data.append({
#         "Title":title,
#         "property_type" : property_type,
#         "price" : price,
#         "area" : area,
#         "purpose" : purpose,
#         "location" : location,
#         "bedrooms" : bedrooms,
#         "bath":bathrooms,
#         "added":added
#     })

# df = pd.DataFrame(all_data)
# print(df)
