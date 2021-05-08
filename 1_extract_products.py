from selenium import webdriver  # for chrome open library for scraping
import time #time library for sleep
from selenium.webdriver.common.keys import Keys  # chrome keys libraries for input forms
from selenium.webdriver.common.action_chains import ActionChains #performing action libraries in chrome like Enter ESC
from bs4 import BeautifulSoup, NavigableString #Libraries to parse HTML

import time
import csv
import os
import argh
from tqdm import tqdm


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    current_dir = os.path.dirname(os.path.realpath(__file__))
    chrome_path = current_dir + '\\chromedriver.exe'
    print(f'Chorme Dirver expected path : {chrome_path}')

    #open chrome browser
    driver = webdriver.Chrome(chrome_path, chrome_options=options)
    return driver

def main(category, total_pages, start_page = 1):

    baseUrl = 'https://www.daraz.pk/'

    d = get_chrome_driver()
    f = open(category + '_urls.csv', 'w', encoding="utf-8")

    daraz = baseUrl + category + '/'
    no_reviews = 0
    total_products = 0

    for i in tqdm(range(start_page, int(total_pages)), desc ="Pages: "):

        try:
            d.get(daraz + '/?page=' + str(i))
        except:
            print("Unable to fetch the url or Timeout")

        src = d.page_source
        soup = BeautifulSoup(src,'html.parser')
        time.sleep(2)
        urll = soup.findAll('div',{'data-qa-locator':'product-item'})

        total_products = total_products + len(urll)


        for i in urll:

            try:
                x = i.find_all('span', class_='c3XbGJ')[0]

                if x:
                    i = i.find('a')
                    f.write(i['href'] + '\n')
            except:
                no_reviews = no_reviews + 1

    d.quit()
    print('\n')
    print(f'Out of {total_products} products, {no_reviews} had no reviews')


if __name__ == '__main__':
    argh.dispatch_command(main)
