# THIS IS PARSER
# IT FINDS ALL ELEMENTS ON WEB PAGE WITH SPECIFIC FILTERS: p, a

import bs4
import requests

# Fetching prices from Web-Page
def get_price(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    price_list = []

    # Find all p-tags
    collector = soup.find_all('p')

    # Sort all founded p tags , and append to the pure list only p-tags with Euro sign in it
    for i in collector:
        text = i.get_text()
        if '€' in text:
            price_list.append(text)

    # Return full list of Prices
    return price_list

# Fetching links from Web-Page
def get_links(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    links_list = []

    # Find all a-tags with className used for specific Links
    collector = soup.find_all('a', class_='absolute inset-0 z-1')

    # Adding Address to the Links and append them to the pure list
    for i in collector:
        # If function return links without https-address , u may add f'https://example-site.com/...'
        full = f'{i['href']}'
        links_list.append(full)

    # Return full list of Links
    return links_list

# Combine price-list and link-list into zipped list for further processing
def data_parser(url):

    prices = get_price(url)
    links = get_links(url)

    data = list(zip(prices, links))

    # return combined List, In formate : ((price1, link1)(price2, link2)...)
    return data

