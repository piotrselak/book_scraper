import sys
from bs4 import BeautifulSoup
import requests

URL: str = 'https://books.toscrape.com/'

def build_url(page_num: int) -> str:
    return URL + f'catalogue/page-{page_num}.html'

def try_parse_argument(ind: int, error_message: str) -> str:
    try:
        return sys.argv[ind]
    except IndexError:
        print(error_message)
        exit(1)

if __name__ == '__main__':
    page = 1
    title = try_parse_argument(1, "You need to pass a book title.")

    response = requests.get(build_url(page))
    books = BeautifulSoup(response.text, 'html.parser').find_all('article', class_='product_pod')

    while response.status_code == 200:
        for book in books:
            bookSoup = BeautifulSoup(str(book), 'html.parser')
            b_title = bookSoup.find('h3').a['title']
            price = bookSoup.find('p', class_='price_color').text[1::]

            if title == b_title:
                print("Price of", b_title, "is", price)
                exit(0)

        page += 1
        response = requests.get(build_url(page))
        books = BeautifulSoup(response.text, 'html.parser').find_all('article', class_='product_pod')


    print("Given book was not found.")