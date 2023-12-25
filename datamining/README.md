# _**PADEL LOVERS**_

Our project consist in scraping a famous e-commerce website 
of padel equipments : [padel-point.com]().

### INSTALLATION

To resolve our project, we used 2 libraries : 
_**grequests**_ and _**BeautifulSoup**_. 
Here is how to install them : 

```bash
pip install grequests
```
```bash
pip install beautifulsoup4
```
Then, you need to import the module _**bs4**_ from beautifulsoup.  
Here is how it looks : 

```python
import grequests
from bs4 import BeautifulSoup
```

### How to run our code ? 

To run our code, you just have to put on the command line : 
```bash
main.py
```
You will get informations about each padel rackets :    
name of the product, its price, the saving and the product number : 

('Speed Junior', '€ 69,95', 'Save 30%', '0060620424000000')

### How did we solve the problem ? 

To scrape datas from [padel-point.com](), here is how we managed to do it :

First of all, we implemented a function named _**get_all_urls()**_ to get urls of every page from the website where we have 
products. 
Then, we got the links of each products from each page with the _**get_link_of_products_page(response)**_ function. 
After that, we got the links of each product from every page with the _**get_every_link()**_ function.
Then, we sent requests for each link with the _**send_requests_on_products()**_ function. 
Finally, we obtained each information we want for each product with the _**get_all_infos()**_ function. 

## THE TEAM

The team is composed by [Sacha Koskas](https://www.linkedin.com/in/sacha-koskas-a3a46b1b5/) and [Dan Finel](https://www.linkedin.com/in/dan-finel/). 
We are both students at ITC ( Israel Technology Challenge).

 

## Contributing 

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

`Please make sure to update tests as appropriate.`



## About the CLI

There are 3 possibles arguments that can be passed on the CLI. 

The first one is :
```bash
'-all','--scrape_everything'
```
Values can be either 'yes' or 'no'. It gives the possibility to whether scrape everything or not.

The second one is :
```bash
'-n','--number_of_product_to_scrape'
```
The value has to be between 1 and the number of padel rackets product on the website (which is 900).
The default value is **None**.
It asks how many products you can to scrape attributes.

The third one is :
```bash
'-cd','--create_database'
```
Values can be either 'yes' or 'no'.
The default Value is **None**.
It creates the database if specified. 


## About the database 

The name of the database is _**datamining_padel**_.
It is composed of 6 tables :
1. Stock
2. Collection
3. Dimension
4. Colors
5. Gender
6. Padel_racket

Let's dive into the first table : 
#### _**Stock**_
The table Stock is composed of an auto-increment index named _id_ and a column
named in_stock which takes two values : _'yes'_ and _'no'_.
It tells us if the product is in stock or not. 

#### _**Collection**_
The table Collection is composed of an auto-increment index named _id_ and a column
named collection which is composed of strings corresponding to the collection of the product.

#### _**Dimension**_
The table Dimension is composed of an auto-increment index named _id_ and 4 floats which correspond to the dimension of the 
product : _profile_,_length_,_head_size_,_balance_.

#### _**Colors**_
The table Colors is composed of an auto-increment index named _id_ and a column named
_color_ which each rows contains a color as a string that can be the first, the second or the third color of the product.

#### _**Gender**_
The table Gender is composed of an auto-increment index named _id_ and 
a column named _gender_ which each rows contains a gender as a string which corresponds to the gender the product is for (_unisex_,_men_,_women_,...).


#### _**Padel_racket**_
The table Padel_racket is composed of an auto-increment index named _id_, 4 attributes named 
_name_,_original_price_,_discounted_price_,_product_number. 

The table is also referencing to each other tables with foreign keys : 
gender_id,first_color_id,second_color_id,third_color_id,stock_id,dimension_id,
collection_id.

Click [here](https://dbdiagram.io/d/6577137a56d8064ca0cbfced) for an ERD diagram of our database datamining_padel.






