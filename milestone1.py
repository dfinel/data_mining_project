import grequests
import sys
from bs4 import BeautifulSoup
from import_json import format_url
from import_json import upper_range_nbr_product
from import_json import nbr_product_per_page
from import_json import number_of_threads
from import_json import url_website
from import_json import good_response
from tqdm import tqdm


def get_all_urls():
    """ Returns urls of each page of padel rackets from the website """
    url = format_url
    return [url.format(i) for i in range(0, upper_range_nbr_product, nbr_product_per_page)]


def get_link_of_products_page(response):
    """ returns the links of each product page from a specific page"""
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except AttributeError:
        raise AttributeError("The url given is not working. Please check it.")
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


def find_attributes(response, flag, class_, itemprop=None):
    """ Returns the text corresponding to an attribute of the product """
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find(flag, class_=class_, itemprop=itemprop).text.strip()


def find_all_attributes(response, flag, class_):
    """ Returns all attributes of the product corresponding to the class"""
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find_all(flag, class_=class_)


def get_attributes(response):
    """ Returns the attributes of our product in a dictionary. The key corresponds tot he name of the attributes and
    the value is the content"""
    attributes = {}
    # Extracting product details
    attributes["name"] = find_attributes(response, "span", "product-name-sub", "name")
    attributes["price"] = find_attributes(response, "span", "value", "price")
    try:
        attributes["saving"] = find_attributes(response, "span", "saving")
    except AttributeError:
        attributes["saving"] = str(0)
    # Extracting product attributes
    for title, value in zip(find_all_attributes(response, "span", "attr-title"),
                            find_all_attributes(response, "span", "attr-value")):
        key = title.text.strip()
        attributes[key] = value.text.strip()
    soup = BeautifulSoup(response.content, 'html.parser')
    if soup.find("i", class_="icon icon-attention"):
        attributes["in stock"] = "No"
    else:
        attributes["in stock"] = "Yes"
    return attributes


def get_all_infos():
    """ returns all the info we need about the product """
    try:
        my_requests = send_requests_on_products()
    except AttributeError:
        print("The given url is not working. Please check it.")
        sys.exit()
    info = []
    for various_request in tqdm(my_requests, desc='PROCESSING...'):
        for request in grequests.imap(various_request, size=number_of_threads):
            response = request
            if response.status_code != good_response:
                print(f'Status code is not 200 but {response.status_code}')
                sys.exit()
            attributes = get_attributes(response)
            all_info = [attributes]
            info.extend(all_info)
    return info


def main():
    print(get_all_infos())


if __name__ == '__main__':
    main()
