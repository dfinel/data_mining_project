import grequests
import sys
import pymysql.cursors
import math
from bs4 import BeautifulSoup
from import_json import format_url
from import_json import nbr_product_per_page
from import_json import url_website
from import_json import number_of_threads
from import_json import good_response
from import_json import span_flag
from import_json import use_database
from import_json import host
from import_json import user
from import_json import password
from import_json import html_feature
from import_json import index_price
from tqdm import tqdm
from padel_logger import logger


def send_requests_on_products(number_of_product):
    """ returns the requests created for each product page link"""
    links = get_every_link(number_of_product)
    my_requests = []
    for link in links:
        my_requests.append([grequests.get(each_link) for each_link in link])
    return my_requests


def find_attributes(response, flag, class_, itemprop=None):
    """ Returns the text corresponding to an attribute of the product """
    soup = BeautifulSoup(response.content, html_feature)
    return soup.find(flag, class_=class_, itemprop=itemprop).text.strip()


def find_all_attributes(response, flag, class_):
    """ Returns all attributes of the product corresponding to the class"""
    soup = BeautifulSoup(response.content, html_feature)
    return soup.find_all(flag, class_=class_)


def get_urls_of_page(number_of_page):
    """ Returns urls of the number of  page of padel rackets  we asked from the website """
    url = format_url
    return [url.format(i) for i in range(0, number_of_page * nbr_product_per_page, nbr_product_per_page)]


def get_link_of_products_page(response):
    """ returns the links of each product page from a specific page"""
    try:
        soup = BeautifulSoup(response.content, html_feature)
    except AttributeError as ae:
        logger.error(f'{ae} : The url given is not working. Please check it')
        raise AttributeError("The url given is not working. Please check it.")
    product_links = [url_website + link['href'] for link in soup.find_all('a', class_="link")]
    return product_links


def get_every_link(number_of_product):
    """ returns a list of the link of each product page"""
    links_of_products = []
    upper_int = math.ceil(number_of_product / nbr_product_per_page)
    requests = (grequests.get(url) for url in get_urls_of_page(math.ceil(number_of_product / nbr_product_per_page)))
    responses = grequests.map(requests)
    for response in responses:
        if len(links_of_products) == upper_int - 1:
            to_get = number_of_product - int(number_of_product / nbr_product_per_page) * nbr_product_per_page
            product_links = get_link_of_products_page(response)[:to_get]
            links_of_products.append(product_links)
        else:
            product_links = get_link_of_products_page(response)
            links_of_products.append(product_links)
    return links_of_products


def get_prices(response):
    """ Returns a dictionary with two keys : original_price, discounted_price and the corresponding values """
    attributes = {}
    for title, value in zip(('original_price', 'discounted_price'),
                            find_all_attributes(response, span_flag, "value")):
        price = value.text.strip()[index_price:]
        price = price.replace(',', '.')
        attributes[title] = float(price)
    return attributes


def get_attributes(response):
    """ Returns the attributes of our product in a dictionary. The key corresponds to the name of the attributes and
    the value is the content"""
    attributes = {'name': find_attributes(response, span_flag, "product-name-sub", "name")}
    attributes.update(get_prices(response))

    # Extracting product attributes
    for title, value in zip(find_all_attributes(response, span_flag, "attr-title"),
                            find_all_attributes(response, span_flag, "attr-value")):
        key = title.text.strip()

        attributes[key] = value.text.strip()

        if key not in ('Product type', 'Sub product type'):  # those attributes are the same for each product
            attributes[key] = value.text.strip()

    soup = BeautifulSoup(response.content, html_feature)
    if soup.find("i", class_="icon icon-attention"):
        attributes["in stock"] = "No"
    else:
        attributes["in stock"] = "Yes"
    return attributes


def get_all_infos(number_of_products):
    """ returns all the info we need about the product """
    try:
        my_requests = send_requests_on_products(number_of_products)

    except AttributeError as ae:
        logger.error(f'{ae} : The url given is not working. Please check it')
        print("The given url is not working. Please check it.")
        sys.exit()
    info = []
    for various_request in tqdm(my_requests, desc='PROCESSING...'):
        for request in grequests.imap(various_request, size=number_of_threads):
            response = request
            if response.status_code != good_response:
                print(f'Status code is not 200 but {response.status_code}')
                logger.error(f'Status code is not 200 but {response.status_code}')
                sys.exit()
            attributes = get_attributes(response)
            all_info = [attributes]
            info.extend(all_info)
    return info


def get_connection():
    """ Returns the connection to access our database """
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_each_attribute(item, name_attribute):
    """ Returns the floated attribute if it exists. None otherwise. """
    attribute = item.get(name_attribute)
    if attribute:
        attribute = float(attribute)
    else:
        attribute = None
    return attribute


def get_dimension_attributes(item):
    """ Returns the profile, length, head_size and balance of our product 'item'."""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        profile = get_each_attribute(item, 'Profile (mm)')
        length = get_each_attribute(item, 'Length (mm)')
        head_size = get_each_attribute(item, 'Head size (cm²)')
        balance = get_each_attribute(item, 'Balance (mm)')
    return profile, length, head_size, balance


def get_part_query(dim_attribute, attribute):
    """ Returns a part of a query that will be used in get_dimension_id"""
    if dim_attribute:
        return f'AND {attribute} = %s '
    else:
        return f'AND {attribute} IS NULL '


def get_dimension_id(cursor, profile, length, head_size, balance):
    """ Returns the id from the table Dimension corresponding to the parameters."""
    query = 'SELECT id FROM Dimension WHERE 1=1 '
    query += (get_part_query(profile, 'profile') + get_part_query(length, 'length') +
              get_part_query(head_size, 'head_size') + get_part_query(balance, 'balance'))
    parameters = [param for param in (profile, length, head_size, balance) if param]
    cursor.execute(query, parameters)
    dimension_id = cursor.fetchone()['id']
    return dimension_id


def get_main_attributes(item):
    """ Returns some attributes of our 'item'."""
    name = item.get('name')
    original_price = item.get('original_price')
    discounted_price = item.get('discounted_price')
    product_number = item.get('Product number')
    return name, original_price, discounted_price, product_number


def get_gender_id(item, cursor):
    """ Returns the id from the table Gender corresponding to the gender we have."""
    gender = item.get('Gender')
    if gender:
        cursor.execute('SELECT id FROM Gender where gender = %s', gender)
        gender_id = cursor.fetchone()['id']
        return gender_id
    else:
        return None


def get_colors_id(item, cursor):
    """ Returns the id of the three colors from the table Colors corresponding to the colors we have."""
    first_color = item.get('1. color')
    if first_color:
        cursor.execute('SELECT id FROM Colors where color = %s', first_color)
        first_color_id = cursor.fetchone()['id']
    else:
        first_color_id = None
    second_color = item.get('2nd Color')
    if second_color:
        cursor.execute('SELECT id FROM Colors where color = %s', second_color)
        second_color_id = cursor.fetchone()['id']
    else:
        second_color_id = None
    third_color = item.get('3rd color')
    if third_color:
        cursor.execute('SELECT id FROM Colors where color = %s', third_color)
        third_color_id = cursor.fetchone()['id']
    else:
        third_color_id = None
    return first_color_id, second_color_id, third_color_id


def get_stock_id(item, cursor):
    """ Returns the id from the table Stock corresponding to the stock we have."""
    stock = item.get('in stock')
    cursor.execute('SELECT id FROM Stock where in_stock = %s', stock)
    stock_id = cursor.fetchone()['id']
    return stock_id


def get_collection_id(item, cursor):
    """ Returns the id from the table Collection corresponding to the collection we have."""
    collection = item.get('Collection')
    if collection:
        cursor.execute('SELECT id FROM Collection where collection = %s', collection)
        collection_id = cursor.fetchone()['id']
    else:
        collection_id = None
    return collection_id
