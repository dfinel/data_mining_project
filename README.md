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
milestone1.py
```
You will get informations about each padel rackets :    
name of the product, its price, the saving and the product number : 

('Speed Junior', '€ 69,95', 'Save 30%', '0060620424000000')

### How did we solve the problem ? 

First of all, we implemented a function named _**get_all_urls()**_ to get urls of every page from the website where we have 
products. 
Then, we got the links of each products from each page with the _**get_link_of_products_page(response)**_ function. 
After that, we got the links of each product from every page with the _**get_every_link()**_ function.
Then, we sent requests for each link with the _**send_requests_on_products()**_ function. 
Finally, we obtained each information we want for each product with the _**get_all_infos()**_ function. 


## Contributing 

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

`Please make sure to update tests as appropriate.





