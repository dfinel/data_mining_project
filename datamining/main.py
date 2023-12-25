import argparse
from import_json import upper_range_nbr_product
from add_to_database import add_data_to_colors
from add_to_database import add_data_to_stock
from add_to_database import add_data_to_gender
from add_to_database import add_data_to_dimension
from add_to_database import add_data_to_collection
from add_to_database import add_attributes_to_padel_rackets
from create_database import create_database
from get_functions import get_all_infos
from amazon_scraping import amazon_add_attributes_padel_racket
from amazon_scraping import amazon_get_all_infos


def create_and_fill_database(data):
    """ Creates the database and fill in the data"""
    create_database()
    add_data_to_colors(data)
    add_data_to_gender(data)
    add_data_to_collection(data)
    add_data_to_dimension(data)
    add_data_to_stock(data)
    add_attributes_to_padel_rackets(data)


def get_all_infos_with_user_parameters():
    """ Takes the arguments from the user to run the code."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-all', '--scrape_everything', type=str, choices=('yes', 'no'),
                        help='Whether to scrape everything or not')
    parser.add_argument('-n', '--number_of_padelp_product_to_scrape', type=int,
                        choices=range(1, upper_range_nbr_product),
                        help="Number of product you want to scrape attributes.", default=None)
    parser.add_argument('-am', '--scrape_amazon_product', type=str,
                        choices=('yes', 'no'),
                        help="Whether to scrape products from amazon or not.", default=None)
    parser.add_argument('-cd', '--create_database', type=str, choices=('yes', 'no'), default=None,
                        help='Create database if specified, otherwise skip')
    args = parser.parse_args()
    if args.scrape_everything and args.create_database and args.scrape_amazon_product:
        all_infos = get_all_infos(upper_range_nbr_product)
        print(all_infos)
        create_and_fill_database(all_infos)
        amazon_add_attributes_padel_racket()

    elif args.number_of_padelp_product_to_scrape and args.create_database and args.scrape_amazon_product:
        get_all = get_all_infos(args.number_of_padelp_product_to_scrape)
        print(get_all)
        create_and_fill_database(get_all)
        amazon_add_attributes_padel_racket()

    elif args.scrape_everything and args.create_database:
        all_infos = get_all_infos(upper_range_nbr_product)
        print(all_infos)
        create_and_fill_database(all_infos)

    elif args.create_database and args.scrape_amazon_product:
        create_database()
        amazon_add_attributes_padel_racket()

    elif args.scrape_everything:
        print(get_all_infos(upper_range_nbr_product))

    elif args.number_of_padelp_product_to_scrape and args.create_database:
        get_all = get_all_infos(args.number_of_padelp_product_to_scrape)
        print(get_all)
        create_and_fill_database(get_all)

    elif args.create_database:
        create_database()

    elif args.number_of_padelp_product_to_scrape:
        print(get_all_infos(args.number_of_padelp_product_to_scrape))

    elif args.scrape_amazon_product:
        print(amazon_get_all_infos())


def main():
    get_all_infos_with_user_parameters()


if __name__ == '__main__':
    main()
