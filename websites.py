'''
Website list
'''
import logging
import requests


SITE_LIST = ['https://envato.com', 'http://amazon.co.uk',
             'http://amazon.com', 'http://facebook.com', 'http://google.com',
             'http://google.fr', 'http://google.es', 'http://google.co.uk',
             'http://internet.org', 'http://gmail.com',
             'http://stackoverflow.com', 'http://github.com',
             'http://heroku.com', 'http://really-cool-available-domain.com',
             'http://djangoproject.com', 'http://rubyonrails.org',
             'http://basecamp.com', 'http://trello.com',
             'http://yiiframework.com', 'http://shopify.com',
             'http://another-really-interesting-domain.co',
             'http://airbnb.com', 'http://instagram.com',
             'http://snapchat.com', 'http://youtube.com', 'http://baidu.com',
             'http://yahoo.com', 'http://live.com', 'http://linkedin.com',
             'http://yandex.ru', 'http://netflix.com', 'http://wordpress.com',
             'http://bing.com'
             ]


def check_website(address, timeout=20):
    '''
    Check if a website is down. A website is considered down
    if either the status_code >= 400 or if the timeout expires

    Throw a WebsiteDownException if any of the website down conditions are met
    '''
    try:
        response = requests.head(address, timeout=timeout)
        if response.status_code >= 400:
            logging.warning('Website %s returned status_code=%s', address,
                            response.status_code)
    except requests.exceptions.RequestException:
        logging.warning('Timeout expired for website %s', address)
