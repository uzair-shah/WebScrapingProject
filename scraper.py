import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time
import sqlite3

data = []
page_num = 1

while True:
    url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Stopped at page {page_num} (status {response.status_code})")
        break
    
    #Extract page
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article',class_ = 'product_pod') #List of all books in html format
    
    word_2_num = {'One':1, 'Two': 2, 'Three':3, 'Four': 4, 'Five':5}
    

    #Parses single page from html to df
    for book in books:
        name = book.find('h3').find('a')['title'] #name of book
        price = float(book.find('div', class_ = 'product_price').find('p', class_ = 'price_color').text.strip("£")) #book price
        in_stock = book.find('p', class_ = 'instock availability').text.strip() #instock
        
        rating_words = book.find('p')['class'][1] #star rating
        rating = 0
        if rating_words in word_2_num: #Converting to integer value
            rating = word_2_num[rating_words]

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


#Linking dataframe to sql 
conn = sqlite3.connect("books.db" ) #connection to an SQLite database called books.

with sqlite3.connect("books.db") as conn:
    df.to_sql('books',conn, if_exists = "replace",index = False)

    #Checking if sql query works
    result = pd.read_sql("SELECT * FROM books WHERE price < 20 ORDER BY price", conn)
print(result.head())
