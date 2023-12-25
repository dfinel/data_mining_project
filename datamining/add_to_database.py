from get_functions import get_connection
from get_functions import get_dimension_attributes
from get_functions import get_collection_id
from get_functions import get_colors_id
from get_functions import get_dimension_id
from get_functions import get_gender_id
from get_functions import get_main_attributes
from get_functions import get_stock_id
from padel_logger import logger
from import_json import use_database
from import_json import padel_point_main_insert_query


def add_data_to_stock(data):
    """ Adds items from 'data' to the table Stock if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        for item in data:
            stock = item.get('in stock')
            if stock:
                query = 'INSERT IGNORE INTO Stock(in_stock) VALUES (%s)'
                cursor.execute(query, (stock,))
    connection.commit()


def add_data_to_gender(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        for item in data:
            gender = item.get('Gender')
            if gender:
                query = 'INSERT IGNORE INTO Gender(gender) VALUES (%s)'
                cursor.execute(query, (gender,))
    connection.commit()


def add_data_to_collection(data):
    """ Adds items from 'data' to the table Collection if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        for item in data:
            collection = item.get('Collection')
            if collection:
                query = 'INSERT IGNORE INTO Collection(collection) VALUES (%s)'
                cursor.execute(query, (collection,))
    connection.commit()


def add_data_to_dimension(data):
    """ Adds items from 'data' to the table Dimension if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        for item in data:
            profile, length, head_size, balance = get_dimension_attributes(item)
            query = 'INSERT IGNORE INTO Dimension(profile,length,head_size,balance) VALUES (%s, %s, %s, %s)'
            cursor.execute(query, (profile, length, head_size, balance))
    connection.commit()


def add_data_to_colors(data):
    """ Adds items from 'data' to the table Colors if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        for item in data:
            first_color = item.get('1. color')
            second_color = item.get('2nd Color')
            third_color = item.get('3rd Color')
            if first_color:
                query = 'INSERT IGNORE INTO Colors(color) VALUES (%s)'
                cursor.execute(query, (first_color,))
            if second_color:
                query = 'INSERT IGNORE INTO Colors(color) VALUES (%s)'
                cursor.execute(query, (second_color,))
            if third_color:
                query = 'INSERT IGNORE INTO Colors(color) VALUES (%s)'
                cursor.execute(query, (third_color,))
    connection.commit()


def add_attributes_to_padel_rackets(data):
    """ Adds items from 'data' to the table Padel_racket if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        for item in data:
            name, original_price, discounted_price, product_number = get_main_attributes(item)
            id_gender = get_gender_id(item, cursor)
            first_color_id, second_color_id, third_color_id = get_colors_id(item, cursor)
            stock_id = get_stock_id(item, cursor)
            profile, length, head_size, balance = get_dimension_attributes(item)
            dimension_id = get_dimension_id(cursor, profile, length, head_size, balance)
            collection_id = get_collection_id(item, cursor)
            query = padel_point_main_insert_query
            cursor.execute(query, (id_gender, first_color_id, second_color_id, third_color_id, stock_id, dimension_id,
                                   collection_id, name, original_price, discounted_price, product_number))
            logger.info(f'{id_gender, first_color_id, second_color_id, third_color_id, stock_id, dimension_id,collection_id, name, original_price, discounted_price, product_number} successfully added to table Padel_racket')
    connection.commit()
