import grequests
import sys
import requests
from bs4 import BeautifulSoup
from import_json import format_url
from import_json import upper_range_nbr_product
from import_json import nbr_product_per_page
from import_json import number_of_threads
from import_json import url_website
from import_json import good_response
from tqdm import tqdm
import argparse
import math
import pymysql.cursors
from create_database import create_database





def get_urls_of_page(number_of_page):
    """ Returns urls of the number of  page of padel rackets  we asked from the website """
    url = format_url
    return [url.format(i) for i in range(0, number_of_page * nbr_product_per_page, nbr_product_per_page)]


def get_link_of_products_page(response):
    """ returns the links of each product page from a specific page"""
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except AttributeError:
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


def send_requests_on_products(number_of_product):
    """ returns the requests created for each product page link"""
    links = get_every_link(number_of_product)
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


def get_prices(response):
    """ Returns a dictionary with two keys : original_price, discounted_price and the corresponding values """
    attributes = {}
    for title, value in zip(('original_price', 'discounted_price'),
                            find_all_attributes(response, "span", "value")):
        price = value.text.strip()[2:]
        price = price.replace(',', '.')
        attributes[title] = float(price)
    return attributes


def get_attributes(response):
    """ Returns the attributes of our product in a dictionary. The key corresponds to the name of the attributes and
    the value is the content"""
    attributes = {'name': find_attributes(response, "span", "product-name-sub", "name")}
    attributes.update(get_prices(response))

    # Extracting product attributes
    for title, value in zip(find_all_attributes(response, "span", "attr-title"),
                            find_all_attributes(response, "span", "attr-value")):
        key = title.text.strip()

        attributes[key] = value.text.strip()

        if key not in ('Product type', 'Sub product type'):  # those attributes are the same for each product
            attributes[key] = value.text.strip()

    soup = BeautifulSoup(response.content, 'html.parser')
    if soup.find("i", class_="icon icon-attention"):
        attributes["in stock"] = "No"
    else:
        attributes["in stock"] = "Yes"

    return attributes


def get_all_infos(number_of_products):
    """ returns all the info we need about the product """
    try:
        my_requests = send_requests_on_products(number_of_products)

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


def get_connection():
    """ Returns the connection to access our database """
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        cursorclass=pymysql.cursors.DictCursor)
    return connection


def add_data_to_stock(data):
    """ Adds items from 'data' to the table Stock if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('USE datamining_padel')
        for item in data:
            stock = item.get('in stock')
            query = 'SELECT COUNT(*) FROM Stock WHERE in_stock = %s'
            cursor.execute(query, stock)
            count = cursor.fetchone()
            if count['COUNT(*)'] == 0:
                cursor.execute('INSERT INTO Stock(in_stock) VALUES (%s)', stock)
    connection.commit()


def add_data_to_gender(data):
    """ Adds items from 'data' to the table Gender if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('USE datamining_padel')
        for item in data:
            gender = item.get('Gender')
            if gender:
                query = 'SELECT COUNT(*) FROM Gender where gender = %s'
                cursor.execute(query, gender)
                count = cursor.fetchone()
                if count['COUNT(*)'] == 0:
                    cursor.execute("INSERT INTO Gender(gender) VALUES (%s)", gender)
    connection.commit()


def add_data_to_collection(data):
    """ Adds items from 'data' to the table Collection if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('USE datamining_padel')
        for item in data:
            collection = item.get('Collection')
            if collection:
                query = f"SELECT COUNT(*) FROM Collection where collection = '{collection}'"
                cursor.execute(query)
                count = cursor.fetchone()
                if count['COUNT(*)'] == 0:
                    cursor.execute("INSERT INTO Collection(collection) VALUES (%s)", collection)
    connection.commit()


def get_dimension_attributes(item):
    """ Returns the profile, length, head_size and balance of our product 'item'."""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('USE datamining_padel')
        profile = item.get('Profile (mm)')
        if profile:
            profile = float(profile)
        else:
            profile = None
        length = item.get('Length (mm)')
        if length:
            length = float(length)
        else:
            length = None
        head_size = item.get('Head size (cm²)')
        if head_size:
            head_size = float(head_size)
        else:
            head_size = None
        balance = item.get('Balance (mm)')
        if balance:
            balance = float(balance)
        else:
            balance = None
    return (profile, length, head_size, balance)


def add_data_to_dimension(data):
    """ Adds items from 'data' to the table Dimension if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('USE datamining_padel')
        for item in data:
            profile, length, head_size, balance = get_dimension_attributes(item)
            query = 'SELECT COUNT(*) FROM Dimension WHERE profile = %s AND length = %s AND head_size = %s AND balance = %s'
            cursor.execute(query, (profile, length, head_size, balance))
            count = cursor.fetchone()
            if count['COUNT(*)'] == 0:
                cursor.execute("INSERT INTO Dimension(profile, length, head_size, balance) VALUES (%s, %s, %s, %s)",
                               (profile, length, head_size, balance))
    connection.commit()


def add_data_to_colors(data):
    """ Adds items from 'data' to the table Colors if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('USE datamining_padel')
        for item in data:
            first_color = item.get('1. color')
            second_color = item.get('2nd Color')
            third_color = item.get('3rd Color')
            if first_color:
                cursor.execute('SELECT COUNT(*) FROM Colors WHERE color = %s', first_color)
                count = cursor.fetchone()
                if count['COUNT(*)'] == 0:
                    cursor.execute('INSERT INTO Colors(color) VALUES (%s)', first_color)
            if second_color:
                cursor.execute('SELECT COUNT(*) FROM Colors WHERE color = %s', second_color)
                count = cursor.fetchone()
                if count['COUNT(*)'] == 0:
                    cursor.execute('INSERT INTO Colors(color) VALUES (%s)', second_color)
            if third_color:
                cursor.execute('SELECT COUNT(*) FROM Colors WHERE color = %s', third_color)
                count = cursor.fetchone()
                if count['COUNT(*)'] == 0:
                    cursor.execute('INSERT INTO Colors(color) VALUES (%s)', third_color)
    connection.commit()


def get_dimension_id(cursor, profile, length, head_size, balance):
    """ Returns the id from the table Dimension corresponding to the parameters."""
    query = 'SELECT id FROM Dimension WHERE 1=1 '
    parameters = []
    if profile:
        query += 'AND profile = %s '
        parameters.append(profile)
    else:
        query += 'AND profile IS NULL '
    if length:
        query += 'AND length = %s '
        parameters.append(length)
    else:
        query += 'AND length IS NULL '
    if head_size:
        query += 'AND head_size = %s '
        parameters.append(head_size)
    else:
        query += 'AND head_size IS NULL '
    if balance:
        query += 'AND balance = %s '
        parameters.append(balance)
    else:
        query += 'AND balance IS NULL '
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


def get_main_count_query():
    """ Returns the main query we will use to know if those attributes exists in the table Padel_racket or not."""
    query = """
        SELECT COUNT(*) FROM Padel_racket WHERE 
        (gender_id IS NULL OR gender_id= %s) AND first_color_id = %s AND 
        (second_color_id IS NULL OR second_color_id = %s) AND 
        (third_color_id IS NULL OR third_color_id = %s) AND 
        stock_id = %s AND dimension_id = %s AND 
        collection_id = %s AND name = %s AND 
        original_price = %s AND discounted_price = %s AND 
        product_number = %s
    """
    return query


def get_main_insert_query():
    """ Returns the query that will allow us to insert data in the table Padel_racket."""
    query = """
    INSERT INTO Padel_racket(gender_id, first_color_id, second_color_id, third_color_id, stock_id, dimension_id, 
    collection_id, name, original_price, discounted_price, product_number)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return query


def add_attributes_to_padel_rackets(data):
    """ Adds items from 'data' to the table Padel_racket if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('USE datamining_padel')
        for item in data:
            name, original_price, discounted_price, product_number = get_main_attributes(item)
            id_gender = get_gender_id(item, cursor)
            first_color_id, second_color_id, third_color_id = get_colors_id(item, cursor)
            stock_id = get_stock_id(item, cursor)
            profile, length, head_size, balance = get_dimension_attributes(item)
            dimension_id = get_dimension_id(cursor, profile, length, head_size, balance)
            collection_id = get_collection_id(item, cursor)
            query = get_main_count_query()
            cursor.execute(query, (id_gender, first_color_id, second_color_id, third_color_id, stock_id, dimension_id,
                                   collection_id, name, original_price, discounted_price, product_number))
            count = cursor.fetchone()
            if count['COUNT(*)'] == 0:
                query = get_main_insert_query()
                cursor.execute(query,
                               (id_gender, first_color_id, second_color_id, third_color_id, stock_id, dimension_id,
                                collection_id, name, original_price, discounted_price, product_number))
    connection.commit()


def create_the_database():
    """ Creates the database without adding any values into it"""
    create_database()


def create_and_fill_database(data):
    """ Creates the database and fill in the data"""
    create_database()
    add_data_to_colors(data)
    add_data_to_gender(data)
    add_data_to_collection(data)
    add_data_to_dimension(data)
    add_data_to_stock(data)
    add_attributes_to_padel_rackets(data)



def process_amazon_product_data(product):
    processed_data = {}
    processed_data['amazon_product_title'] = product.get('product_title', '')
    processed_data['amazon_product_original_price'] = float(
        product.get('product_original_price', '0').replace('$', '').replace(',', ''))
    processed_data['amazon_product_num_ratings'] = int(product.get('product_num_ratings', 0))
    processed_data['amazon_product_star_rating'] = float(product.get('product_star_rating', 0))
    processed_data['amazon_product_minimum_offer_price'] = float(
        product.get('product_minimum_offer_price', '0').replace('$', '').replace(',', ''))
    processed_data['amazon_is_prime'] = product.get('is_prime', False)
    sales_volume = product.get('sales_volume', '')
    processed_data['amazon_sales_volume'] = int(sales_volume.split()[0]) if sales_volume else 0
    return processed_data

def add_amazon_data_to_padel_rackets(amazon_data):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('USE datamining_padel')
        for product_data in amazon_data:
            product = process_amazon_product_data(product_data)

            # Check if the product already exists in the database by a unique field, such as name or product_number
            cursor.execute('SELECT id FROM Padel_racket WHERE name = %s', (product['amazon_product_title'],))
            result = cursor.fetchone()

            # If the product does not exist, insert it
            if not result:
                insert_query = """
                INSERT INTO Padel_racket (
                    amazon_product_title,
                    amazon_product_original_price,
                    amazon_product_num_ratings,
                    amazon_product_star_rating,
                    amazon_product_minimum_offer_price,
                    amazon_is_prime,
                    amazon_sales_volume
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    product['amazon_product_title'],
                    product['amazon_product_original_price'],
                    product['amazon_product_num_ratings'],
                    product['amazon_product_star_rating'],
                    product['amazon_product_minimum_offer_price'],
                    product['amazon_is_prime'],
                    product['amazon_sales_volume']
                ))
            else:
                # If the product exists, update it
                update_query = """
                UPDATE Padel_racket SET
                    amazon_product_original_price = %s,
                    amazon_product_num_ratings = %s,
                    amazon_product_star_rating = %s,
                    amazon_product_minimum_offer_price = %s,
                    amazon_is_prime = %s,
                    amazon_sales_volume = %s
                WHERE name = %s
                """
                cursor.execute(update_query, (
                    product['amazon_product_original_price'],
                    product['amazon_product_num_ratings'],
                    product['amazon_product_star_rating'],
                    product['amazon_product_minimum_offer_price'],
                    product['amazon_is_prime'],
                    product['amazon_sales_volume'],
                    product['amazon_product_title']
                ))
        connection.commit()


def create_and_fill_database(data):
    create_database()
    add_data_to_colors(data)
    add_data_to_gender(data)
    add_data_to_collection(data)
    add_data_to_dimension(data)
    add_data_to_stock(data)
    add_attributes_to_padel_rackets(data)
    amazon_data = fetch_amazon_data()
    add_amazon_data_to_padel_rackets(amazon_data)




def fetch_amazon_data():
    all_products = []
    page = 1
    while True:
        url = "https://real-time-amazon-data.p.rapidapi.com/search"
        querystring = {"query":"padel racket","page":str(page),"country":"US","category_id":"sporting"}
        headers = {
            "X-RapidAPI-Key": "04416a7631msh804ef624733c365p16c86fjsn0ba96cdcd2f4",
            "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        # print(f"Status Code: {response.status_code}")  # To debug
        # print(f"Response: {response.text}")  # To debug
        if response.status_code != 200:
            # Handle non-successful responses or add retry logic
            break
        data = response.json()
        all_products.extend(data.get('data', []))
        if len(data.get('items', [])) < 14:  # Assuming 14 is the max number of items per page
            break
        page += 1
    return all_products


print(fetch_amazon_data())
def add_amazon_data_to_padel_rackets(amazon_data):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('USE datamining_padel')
        for product_data in amazon_data:
            product = process_amazon_product_data(product_data)

            # Check if the product already exists in the database by a unique field, such as name or product_number
            cursor.execute('SELECT id FROM Padel_racket WHERE name = %s', (product['amazon_product_title'],))
            result = cursor.fetchone()

            # If the product does not exist, insert it
            if not result:
                insert_query = """
                INSERT INTO Padel_racket (
                    amazon_product_title,
                    amazon_product_original_price,
                    amazon_product_num_ratings,
                    amazon_product_star_rating,
                    amazon_product_minimum_offer_price,
                    amazon_is_prime,
                    amazon_sales_volume
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    product['amazon_product_title'],
                    product['amazon_product_original_price'],
                    product['amazon_product_num_ratings'],
                    product['amazon_product_star_rating'],
                    product['amazon_product_minimum_offer_price'],
                    product['amazon_is_prime'],
                    product['amazon_sales_volume']
                ))
            else:
                # If the product exists, update it
                update_query = """
                UPDATE Padel_racket SET
                    amazon_product_original_price = %s,
                    amazon_product_num_ratings = %s,
                    amazon_product_star_rating = %s,
                    amazon_product_minimum_offer_price = %s,
                    amazon_is_prime = %s,
                    amazon_sales_volume = %s
                WHERE name = %s
                """
                cursor.execute(update_query, (
                    product['amazon_product_original_price'],
                    product['amazon_product_num_ratings'],
                    product['amazon_product_star_rating'],
                    product['amazon_product_minimum_offer_price'],
                    product['amazon_is_prime'],
                    product['amazon_sales_volume'],
                    product['amazon_product_title']
                ))
        connection.commit()

def get_all_infos_with_user_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('-all', '--scrape_everything', type=str, choices=('yes', 'no'),
                        help='Whether to scrape everything or not')
    parser.add_argument('-n', '--number_of_product_to_scrape', type=int, choices=range(1, upper_range_nbr_product),
                        help="Number of product you want to scrape attributes.", default=None)
    parser.add_argument('-cd', '--create_database', type=str, choices=('yes', 'no'), default=None,
                        help='Create database if specified, otherwise skip')
    args = parser.parse_args()
    if args.scrape_everything and args.create_database:
        product_data = get_all_infos(upper_range_nbr_product)  # Fetch all product data
        create_and_fill_database(product_data)  # Fill the database with scraped and API data
    elif args.scrape_everything:
        print(get_all_infos(upper_range_nbr_product))
    elif args.number_of_product_to_scrape and args.create_database:
        get_all = get_all_infos(args.number_of_product_to_scrape)
        create_and_fill_database(get_all)
    elif args.create_database:
        create_database()
    elif args.number_of_product_to_scrape:
        print(get_all_infos(args.number_of_product_to_scrape))


# def main():
#     get_all_infos_with_user_parameters()
#
#
# if __name__ == '__main__':
#     main()


