import grequests
from bs4 import BeautifulSoup
from import_json import format_url
from import_json import upper_range_nbr_product
from import_json import nbr_product_per_page
from import_json import number_of_threads
from import_json import url_website
from import_json import good_response



def get_all_urls():
    """ Returns urls of each page of padel rackets from the website """
    url = format_url
    return [url.format(i) for i in range(0, upper_range_nbr_product, nbr_product_per_page)]


def get_link_of_products_page(response):
    """ returns the links of each product page from a specific page"""
    soup = BeautifulSoup(response.content, 'html.parser')
    product_links = [url_website + link['href'] for link in soup.find_all('a', class_="link")]
    return product_links


def get_every_link():
    """ returns a list of the link of each product page"""
    all_links = []
    requests = (grequests.get(url) for url in get_all_urls())
    responses = grequests.map(requests)
    for response in responses:
        product_links = get_link_of_products_page(response)
        all_links.append(product_links)
    return all_links


def send_requests_on_products():
    """ returns the requests created for each product page link"""
    links = get_every_link()
    my_requests = []
    for link in links:
        my_requests.append([grequests.get(each_link) for each_link in link])
    return my_requests


def get_all_infos():
    """ returns all the info we need about the product : name, price, saving, and the reference of the product"""
    my_requests = send_requests_on_products()
    info = []
    for various_request in my_requests:
        for request in grequests.imap(various_request, size=number_of_threads):
            response = request
            if response.status_code != good_response:
                raise FileExistsError(f'Status code is not 200 but {response.status_code}')
            soup = BeautifulSoup(response.content, 'html.parser')
            product_number = soup.find_all("span", class_="attr-value product-id")
            name = soup.find_all("span", class_="product-name-sub", itemprop="name")
            price = soup.find_all("span", class_="value", itemprop="price")
            saving = soup.find_all("span", class_="saving")
            all_info = [(each_name.text.strip(), each_price.text.strip(), each_saving.text.strip(),
                         each_product_details.text.strip()) for
                        each_name, each_price, each_saving, each_product_details in
                        zip(name, price, saving, product_number)]
            for infor in all_info:
                print(infor)
    return info
get_all_infos()
#
#
# def send_requests():
#     """ returns the requests and set the header to avoid code repetition"""
#     # headers = {'User-Agent': 'Your User Agent', }
#     links = get_all_urls()
#     my_requests = [grequests.get(link) for link in links]  # creates the request
#     return my_requests
#
#
# def get_price_and_name():
#     requests = send_requests()
#     prices_and_names = []
#     for request in grequests.imap(requests, size=10):
#         response = request
#         soup = BeautifulSoup(response.content, 'html.parser')
#         price = soup.find_all('span', itemprop="price")
#         name = soup.find_all("a", class_="link", itemprop="url")
#         name_and_price = [(each_name.text.strip(),each_price.text.strip()) for each_name,each_price in zip(name,price)]
#         prices_and_names.append(name_and_price)
#     return prices_and_names
