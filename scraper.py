import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

url = "https://books.toscrape.com"
response = requests.get(url)
response.encoding = 'utf-8'
df = pd.DataFrame(columns=['book_name','link'])


soup = BeautifulSoup(response.text, 'html.parser')

books = soup.find_all('article',class_ = 'product_pod') #books are enclosed in article tag with class product_pod

data = []

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
df = pd.DataFrame(data)
print(df)