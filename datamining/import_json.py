import json


def load_config(filename):
    with open(filename) as json_file:
        return json.load(json_file)


config = load_config('config.json')
format_url = config["format_of_url"]
upper_range_nbr_product = config["upper_range_number_of_product"]
nbr_product_per_page = config["number_of_product_per_page"]
number_of_threads = config["number of threads"]
url_website = config["url_of_website"]
good_response = config["good_response"]
host = config["host"]
user = config["user"]
password = config["password"]
amazon_url = config["amazon_url"]
amazon_headers = config["amazon_headers"]
amazon_main_insert_query = config["amazon_main_insert_query"]
amazon_main_update_query = config["amazon_main_update_query"]
use_database = config["use_database"]
amazon_pages_to_scrape = config["amazon_pages_to_scrape"]
amazon_min_page_to_scrape = config["amazon_min_page_to_scrape"]
html_feature = config["html_feature"]
span_flag = config["span_flag"]
easy_query = config["easy_query"]
padel_point_main_insert_query = config["padel_point_main_insert_query"]
index_price = config['index_price']
padel_point_main_count_query = config["padel_point_main_count_query"]