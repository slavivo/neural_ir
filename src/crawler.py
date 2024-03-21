'''
This script is used to crawl the data from the web specifically from the website 
https://zidle-stolicky.heureka.cz/
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import re
import json
import logging
import sys
import argparse

# Set up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
base_url = 'https://zidle-stolicky.heureka.cz/'
base_path = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(base_path, '../data/')
output_file = os.path.join(output_path, 'data.csv')


def get_page(url):
    '''
    This function is used to get the page content of the given url.

    Parameters:
    url (str): The url of the page.

    Returns:
    bytes: The page content of the given url.
    '''
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            logger.error(f'Failed to get the page content of the url: {url}')
            return None
    except Exception as e:
        logger.error(f'Error occured while getting the page content of the url: {url}')
        logger.error(f'Error: {e}')
        return None
    

def get_product_links(page_content):
    '''
    This function is used to get the product links from the page content.

    Parameters:
    page_content (bytes): The page content of the given url.

    Returns:
    list: The list of product links.
    '''
    try:
        soup = BeautifulSoup(page_content, 'html.parser')
        product_links = [a['href'] for a in soup.find_all('a', class_='c-product__link c-star-rating__rating c-product__rating', href=True)]
        product_links = [link.split('#')[0] + '#specifikace' for link in product_links if link.split('#')[0] != '']
        return product_links
    except Exception as e:
        logger.error(f'Error occured while getting the product links')
        logger.error(f'Error: {e}')
        return None


def get_product_details(page_content):
    '''
    This function is used to get the product details from the page content.

    Parameters:
    page_content (bytes): The page content of the given url.

    Returns:
    dict: The product details.
    '''
    try:
        soup = BeautifulSoup(page_content, 'html.parser')
        product_details = {}
        info = json.loads(soup.find('meta', {'name': 'gtm_additional_data:item'})['content'])
        product_details['name'] = info['name']
        product_details['categories'] = info['category']['names']
        info = json.loads(soup.find('meta', {'name': 'gtm_additional_data:ecommerce'})['content'])
        product_details['price'] = info['items'][0]['item_price']
        product_details['rating'] = info['items'][0]['item_rating']
        specification = soup.find('div', class_='c-editable-content c-editable-content--specification')
        specification = specification.find('p') if specification else None
        product_details['specification'] = specification.text if specification else None
        return product_details
    except Exception as e:
        logger.error(f'Error occured while getting the product details')
        logger.error(f'Error: {e}')
        return None
    

def save_to_csv(data, file_path):
    '''
    This function is used to save the data to a csv file.

    Parameters:
    data (list): The list of data to be saved.
    file_path (str): The file path to save the data.

    Returns:
    None
    '''
    try:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        logger.info(f'Data saved to the file: {file_path}')
    except Exception as e:
        logger.error(f'Error occured while saving the data to the file')
        logger.error(f'Error: {e}')
        return None
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        
    try:
        logger.info('Crawling the data from the website...')
        page_content = get_page(base_url)
        if page_content:
            logger.info('Data crawled successfully, extracting the product links...')
            product_links = get_product_links(page_content)
            if product_links:
                data = []
                logger.debug(f'Product links: {product_links}')
                logger.info('Product links extracted successfully, extracting the product details...')
                for link in product_links:
                    time.sleep(random.randint(1, 3))
                    product_page_content = get_page(link)
                    if product_page_content:
                        product_details = get_product_details(product_page_content)
                        logger.debug(f'Product details: {product_details}')
                        if product_details:
                            data.append(product_details)
                if data:
                    save_to_csv(data, output_file)
    except Exception as e:
        logger.error(f'Error occured while crawling the data from the website')
        logger.error(f'Error: {e}')
        return None
    

if __name__ == '__main__':
    main()
