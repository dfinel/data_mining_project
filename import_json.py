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
