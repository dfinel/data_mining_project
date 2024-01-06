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
from import_json import padel_point_main_count_query

def add_data_to_stock(data):
    """ Adds items from 'data' to the table Stock if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        for item in data:
            stock = item.get('in stock')
            query = 'SELECT COUNT(*) FROM Stock WHERE in_stock = %s'
            cursor.execute(query, stock)
            count = cursor.fetchone()
            if count['COUNT(*)'] == 0:
                cursor.execute('INSERT INTO Stock(in_stock) VALUES (%s)', stock)
    connection.commit()


def add_data_to_gender(data):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        for item in data:
            gender = item.get('Gender')
            if gender:
                query = 'SELECT COUNT(*) FROM Gender where gender = %s'
                cursor.execute(query, gender)
                count = cursor.fetchone()
                if count['COUNT(*)'] == 0:
                    cursor.execute("INSERT INTO Gender(gender) VALUES (%s)", gender)
            connection.commit()
    connection.commit()


def add_data_to_collection(data):
    """ Adds items from 'data' to the table Collection if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
        for item in data:
            collection = item.get('Collection')
            if collection:
                query = f"SELECT COUNT(*) FROM Collection where collection = '{collection}'"
                cursor.execute(query)
                count = cursor.fetchone()
                if count['COUNT(*)'] == 0:
                    cursor.execute("INSERT INTO Collection(collection) VALUES (%s)", collection)
    connection.commit()


def add_data_to_dimension(data):
    """ Adds items from 'data' to the table Dimension if the data does not already exist"""
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(use_database)
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
        cursor.execute(use_database)
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
            query = padel_point_main_count_query
            cursor.execute(query, (id_gender, first_color_id, second_color_id, third_color_id, stock_id, dimension_id,
                                   collection_id, name, original_price, discounted_price, product_number))
            count = cursor.fetchone()
            if count['COUNT(*)'] == 0:
                query = padel_point_main_insert_query
                cursor.execute(query,
                               (id_gender, first_color_id, second_color_id, third_color_id, stock_id, dimension_id,
                                collection_id, name, original_price, discounted_price, product_number))
                logger.info(f'{id_gender, first_color_id, second_color_id, third_color_id, stock_id, dimension_id,collection_id, name, original_price, discounted_price, product_number} successfully added to table Padel_racket')
    connection.commit()
