import pymysql.cursors


def get_the_connection():
    """ Returns the connection to access the database"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root1234',
        cursorclass=pymysql.cursors.DictCursor)
    return connection

def create_database_dataminig_padel():
    """ Creates the database datamining_padel"""
    connection = get_the_connection()
    with connection.cursor() as cursor:
        create_db = 'CREATE DATABASE IF NOT EXISTS datamining_padel'
        cursor.execute(create_db)
        connection.commit()

def create_table_padel_racket():
    """ Creates the Padel_racket table with additional Amazon product data columns """
    connection = get_the_connection()
    with connection.cursor() as cursor:
        cursor.execute("USE datamining_padel")
        create_table = """
        CREATE TABLE IF NOT EXISTS Padel_racket(
            id INT AUTO_INCREMENT PRIMARY KEY,
            gender_id INT,
            first_color_id INT,
            second_color_id INT,
            third_color_id INT,
            stock_id INT,
            dimension_id INT,
            collection_id INT,
            FOREIGN KEY (gender_id) REFERENCES Gender(id),
            FOREIGN KEY (first_color_id) REFERENCES Colors(id),
            FOREIGN KEY (second_color_id) REFERENCES Colors(id),
            FOREIGN KEY (third_color_id) REFERENCES Colors(id),
            FOREIGN KEY (stock_id) REFERENCES Stock(id),
            FOREIGN KEY (dimension_id) REFERENCES Dimension(id),
            FOREIGN KEY (collection_id) REFERENCES Collection(id),
            name VARCHAR(100),
            original_price FLOAT(10,2),
            discounted_price FLOAT(10,2),
            product_number VARCHAR(50),
            amazon_product_title VARCHAR(255),
            amazon_product_original_price FLOAT(10,2),
            amazon_product_num_ratings INT,
            amazon_product_star_rating FLOAT(3,1),
            amazon_product_minimum_offer_price FLOAT(10,2),
            amazon_is_prime BOOLEAN,
            amazon_sales_volume INT
        )
        """
        cursor.execute(create_table)
        connection.commit()


def create_table_gender():
    """ Creates into the database datamining_padel the table Gender"""
    connection = get_the_connection()
    with connection.cursor() as cursor:
        cursor.execute("USE datamining_padel")
        create_table = """
    CREATE TABLE IF NOT EXISTS Gender(
    id INT AUTO_INCREMENT PRIMARY KEY,
    gender VARCHAR(50)
    )
    """
        cursor.execute(create_table)


def create_table_colors():
    """ Creates into the database datamining_padel the table Colors"""
    connection = get_the_connection()
    with connection.cursor() as cursor:
        cursor.execute("USE datamining_padel")
        create_table = """
    CREATE TABLE IF NOT EXISTS Colors(
    id INT AUTO_INCREMENT PRIMARY KEY,
    color VARCHAR(50)
    )
    """
        cursor.execute(create_table)


def create_table_stock():
    """ Creates into the database datamining_padel the table Stock"""
    connection = get_the_connection()
    with connection.cursor() as cursor:
        cursor.execute("USE datamining_padel")
        create_table = """
        CREATE TABLE IF NOT EXISTS Stock(
        id INT AUTO_INCREMENT PRIMARY KEY,
        in_stock VARCHAR(100)
        )
        """
        cursor.execute(create_table)


def create_table_dimension():
    """ Creates into the database datamining_padel the table Dimension"""
    connection = get_the_connection()
    with connection.cursor() as cursor:
        cursor.execute("USE datamining_padel")
        create_table = """
    CREATE TABLE IF NOT EXISTS Dimension(
    id INT AUTO_INCREMENT PRIMARY KEY,
    profile FLOAT(10),
    length FLOAT(10),
    head_size FLOAT(10),
    balance FLOAT(10)  
    )
    """
        cursor.execute(create_table)


def create_table_collection():
    """ Creates into the database datamining_padel the table Collection"""
    connection = get_the_connection()
    with connection.cursor() as cursor:
        cursor.execute("USE datamining_padel")
        create_table = """
    CREATE TABLE IF NOT EXISTS Collection(
    id INT AUTO_INCREMENT PRIMARY KEY,
    collection VARCHAR(100)
    )
    """
        cursor.execute(create_table)




def create_database():
    """ Executes all the previous functions to have the database composed of the tables """
    create_database_dataminig_padel()
    create_table_stock()
    create_table_collection()
    create_table_dimension()
    create_table_colors()
    create_table_gender()
    create_table_padel_racket()
