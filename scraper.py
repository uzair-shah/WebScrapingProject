import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time

data = []
page_num = 1

while True:
    url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
    response = requests.get(url)
    response.encoding = 'utf-8'
    #shortcircuit if end of pages reached
    if response.status_code != 200:
        print(f"Stopped at page {page_num} (status {response.status_code})")
        break
    
    url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
    #Extract page
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article',class_ = 'product_pod') #List of all books in html format
    #Parses single page from html to df
    for book in books:
        name = book.find('h3').find('a')['title'] #name of book
        price = float(book.find('div', class_ = 'product_price').find('p', class_ = 'price_color').text.strip("£")) #book price
        in_stock = book.find('p', class_ = 'instock availability').text.strip() #instock
        rating = book.find('p')['class'][1] #star rating
        rel_link = book.find('div',class_ = 'image_container').find('a').find('img')['src'] #relative link
        link = urljoin(url,rel_link)
        data.append({'name':name, 
                    'price':price, 
                    'in_stock':in_stock, 
                    'rating':rating, 
                    'link':link
                    })
    print(f"Scraped page {page_num}, got {len(books)} books")
    page_num += 1 #go to next page
    time.sleep(0.5) #wait for website
df = pd.DataFrame(data)
df = pd.DataFrame(data)
print(df)