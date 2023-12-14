import pymysql.cursors


def get_the_connection():
    """ Returns the connection to access the database"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        cursorclass=pymysql.cursors.DictCursor)
    return connection

def create_database_dataminig_padel():
    """ Creates the database datamining_padel"""
    connection = get_the_connection()
    with connection.cursor() as cursor:
        create_db = 'CREATE DATABASE IF NOT EXISTS datamining_padel'
        cursor.execute(create_db)

def create_table_padel_racket():
    """ Creates into the database datamining_padel the table padel_racket"""
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
    original_price FLOAT(10),
    discounted_price FLOAT(10),
    product_number VARCHAR(50)
    )
    """
        cursor.execute(create_table)


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

