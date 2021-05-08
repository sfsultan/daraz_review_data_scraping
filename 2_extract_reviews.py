from selenium import webdriver  # for chrome open library for scraping

from selenium.webdriver.common.keys import Keys  # chrome keys libraries for input forms
from selenium.webdriver.common.action_chains import ActionChains #performing action libraries in chrome like Enter ESC
from bs4 import BeautifulSoup, NavigableString #Libraries to parse HTML

import time
import csv
import os
import re

from tqdm import tqdm
from urllib.parse import urlparse
import requests

import argh



def get_chrome_driver():
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    current_dir = os.path.dirname(os.path.realpath(__file__))
    chrome_path = current_dir + '\\chromedriver.exe'
    print(f'Chorme Dirver expected path : {chrome_path}')

    driver = webdriver.Chrome(chrome_path, chrome_options=options)
    return driver


def main(category):

    csv.register_dialect(
        'mydialect',
        delimiter = ',',
        quotechar = '"',
        doublequote = True,
        skipinitialspace = True,
        lineterminator = '\n',
        quoting = csv.QUOTE_MINIMAL)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    chrome_path = current_dir + '\\chromedriver.exe'

    baseUrl = 'https://www.daraz.pk/'

    category_file = open(category + '_urls.csv', 'r', encoding="utf-8")
    r = csv.reader(category_file)
    row_count = sum(1 for row in r)

    category_file.seek(0)
    r = csv.reader(category_file)
    url_list = list(r)
    print("Read the list in")

    reviews_file = open(category + '_reviews.csv', 'a', encoding="utf-8")
    f = csv.writer(reviews_file, dialect='mydialect')

    d = get_chrome_driver()

    countproduct=0

    for i in tqdm(range(0, len(url_list)), desc ="Products: "):
        # try:
        countproduct=countproduct+1
        url=url_list[i][0].replace('\n','')

        URL = 'https:' + str(url)
        parsed_url = urlparse(URL)
        d.get(URL)
        src = d.page_source

        soup = BeautifulSoup(src,'html.parser')
        # time.sleep(2)

        # item_id = soup.find('div',{'class':'pdp-mod-review'})['itemid']
        item_id = re.findall('\-i\d*\-', URL)[0][2:]
        item_id = item_id[:-1]

        brandtitle=''
        if(soup.find('span',{'class':'pdp-mod-product-badge-title'})):
            brandtitle=soup.find('span',{'class':'pdp-mod-product-badge-title'})
            brandtitle=brandtitle.get_text()
            brandtitle=brandtitle.strip()
            brandtitle=brandtitle.replace(',','')
            brandtitle=brandtitle.replace('.','')
            brandtitle=brandtitle.replace('\n','')
            brandtitle=brandtitle.replace('\t','')
            brandtitle=brandtitle.replace('"','')

        brandname=''
        if(soup.find('div',{'class':'pdp-product-brand'})):
            brandname=soup.find('div',{'class':'pdp-product-brand'})
            brandname=brandname.find('a')
            brandname=brandname.get_text()
            brandname=brandname.strip()

        averagerating=''
        if(soup.find('span',{'class':'score-average'})):
            averagerating=soup.find('span',{'class':'score-average'})
            averagerating=averagerating.get_text()
            averagerating=averagerating.strip()


        review_page_number = 1
        while True:
            review_url = 'https://my.daraz.pk/pdp/review/getReviewList?itemId={0}&pageSize={1}&filter=0&sort=0&pageNo={2}'.format(item_id, 2000, review_page_number)
            try:
                response = requests.get(review_url).json()
            except:
                print("Error Reviews")
                print(URL)
                print(item_id)
            reviews_list = response['model']['items']
            review_page_number = review_page_number + 1

            if len(reviews_list) < 1:
                break
            else:
                for i in reviews_list:
                    content = i['reviewContent']
                    f.writerow([item_id ,'Product '+str(countproduct), brandname, brandtitle, URL,averagerating, str(content)])

    d.quit()

if __name__ == '__main__':
    argh.dispatch_command(main)
