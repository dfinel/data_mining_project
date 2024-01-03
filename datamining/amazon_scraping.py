import gevent.monkey
import requests
import re
from get_functions import get_connection
from import_json import amazon_url
from import_json import amazon_headers
from import_json import use_database
from import_json import amazon_main_insert_query
from import_json import amazon_main_update_query
from import_json import amazon_pages_to_scrape
from import_json import amazon_min_page_to_scrape

gevent.monkey.patch_all(thread=False, select=False)


def amazon_response_from_rapid_api(num_page):
    """ Returns the response from the rapid_api api for the given page number"""
    url = amazon_url
    querystring = {"query": "Padel racket", "page": str(num_page), "country": "US", "category_id": "sporting"}
    headers = amazon_headers
    response = requests.get(url, headers=headers, params=querystring)
    return response


def amazon_get_name(product):
    """ Returns a dictionary with the name of the product"""
    attribute = {}
    amazon_name = product.get('product_title', None)
    if amazon_name:
        attribute['amazon_name'] = re.split(r'[-,]', amazon_name)[0]
    return attribute


def amazon_get_price(product, price, amazon_type_price):
    """ Returns a dictionary with the price of the product. It can be the original or the discounted price"""
    attribute = {}
    amazon_price = product.get(price, None)
    if amazon_price:
        attribute[amazon_type_price] = float(amazon_price[1:])
    else:
        attribute[amazon_type_price] = None
    return attribute


def amazon_get_rating(product, rating, amazon_type_rating):
    """ Returns a dictionary with the rating of the product. It can be the star rating or the number or rating"""
    attribute = {}
    amazon_rating = product.get(rating, None)
    if amazon_rating:
        attribute[amazon_type_rating] = float(amazon_rating)
    else:
        attribute[amazon_type_rating] = None
    return attribute


def amazon_get_sales_volume(product, sales_volume, amazon_type_sales_volume):
    """ Returns a dictionary with the sales_volume of the product."""
    attribute = {}
    amazon_sales_volume = product.get(sales_volume, None)
    if amazon_sales_volume:
        attribute[amazon_type_sales_volume] = int((re.split(r'\D+', amazon_sales_volume))[0])
    else:
        attribute[amazon_type_sales_volume] = None
    return attribute


def amazon_get_main_attributes_from_a_product(product):
    """ Returns a dictionary with attributes of the product."""
    attribute = amazon_get_name(product)
    attribute.update(amazon_get_price(product, 'product_original_price', 'amazon_original_price'))
    attribute.update(amazon_get_price(product, 'product_price', 'amazon_discounted_price'))
    attribute.update(amazon_get_rating(product, 'product_star_rating', 'amazon_star_rating'))
    attribute.update(amazon_get_rating(product, 'product_num_ratings', 'amazon_num_ratings'))
    attribute.update(amazon_get_sales_volume(product, 'sales_volume', 'amazon_sales_volume'))
    return attribute


def amazon_get_attributes_from_a_page(nbr_page):
    """ Returns a list of dictionaries with attributes of each product of the given number page."""
    response = amazon_response_from_rapid_api(nbr_page)
    list_dictionary = response.json()
    data = []
    for items in list_dictionary.get('data').get('products'):
        data.append(amazon_get_main_attributes_from_a_product(items))
    return data


def amazon_get_all_infos():
    """ Returns a list of dictionaries with attributes of each product of each page. """
    info = []
    for page in range(amazon_min_page_to_scrape, amazon_pages_to_scrape):
        if amazon_get_attributes_from_a_page(page):
            info.extend(amazon_get_attributes_from_a_page(page))
        else:
            break
    return info


def amazon_get_id_matching_name(amazon_name, cursor):
    """ Return the matching id of the table Padel_racket with a name which has a part of the given amazon_name. """
    cursor.execute(use_database)
    cursor.execute('SELECT id,name,amazon_name from Padel_racket')
    all_name = cursor.fetchall()
    if amazon_name:
        split_name = amazon_name.split()
        for dict in all_name:
            name = dict.get('name')
            if name:
                amaz_name = dict.get('amazon_name')
                for part_of_name in split_name:
                    if part_of_name in name and not amaz_name:
                        return dict.get('id')
    return 0


def amazon_add_attributes_padel_racket():
    """ Add all the attributes from amazon for each product to the existing database datamining_padel."""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        data = amazon_get_all_infos()
        for elem in data:
            id = amazon_get_id_matching_name(elem.get('amazon_name'), cursor)
            tuple_values = tuple(elem.values())
            if id == 0:
                query = amazon_main_insert_query
                cursor.execute(query, tuple_values)
            else:
                query = amazon_main_update_query
                cursor.execute(query, tuple_values + (id,))
    connection.commit()


