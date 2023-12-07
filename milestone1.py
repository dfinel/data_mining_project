import grequests
import sys
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


def get_all_infos():
    """ returns all the info we need about the product """
    try:
        my_requests = send_requests_on_products()
    except AttributeError:
        print("The given url is not working. Please check it.")
        sys.exit()
    info = []
    for various_request in my_requests:
        for request in grequests.imap(various_request, size=number_of_threads):
            response = request
            if response.status_code != good_response:
                raise FileExistsError(f'Status code is not 200 but {response.status_code}')
            soup = BeautifulSoup(response.content, 'html.parser')
            attributes = {}

            # Extracting product details
            attributes["name"] = soup.find("span", class_="product-name-sub", itemprop="name").text.strip()
            attributes["price"] = soup.find("span", class_="value", itemprop="price").text.strip()

            try:
                attributes["saving"] = soup.find("span", class_="saving").text.strip()
            except AttributeError:
                attributes["saving"] = str(0)

            # Extracting product attributes
            for title, value in zip(soup.find_all("span", class_="attr-title"),
                                    soup.find_all("span", class_="attr-value")):
                key = title.text.strip()
                attributes[key] = value.text.strip()

            if soup.find("i", class_="icon icon-attention"):
                attributes["in stock"] = "No"
            else:
                attributes["in stock"] = "Yes"

            all_info = [attributes]
            info.extend(all_info)
            print(info)
    return info


def main():
   get_all_infos()


if __name__ == '__main__':
    main()
