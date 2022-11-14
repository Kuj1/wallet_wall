from config import Config

import time
import os
import concurrent.futures
import shutil
from multiprocessing import cpu_count

from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


data_folder = os.path.join(os.getcwd(), 'result_data')
get_folder = os.path.join(os.getcwd(), 'uploaded_file')


if not os.path.exists(data_folder):
    os.mkdir(data_folder)

ua = UserAgent(verify_ssl=False)

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'--user-agent={ua.random}')
options.add_argument('start-maximized')
options.add_argument('--headless')
options.add_argument('--enable-javascript')


def rename(path):
    ls_file = os.listdir(path)[0]
    os.rename(os.path.join(path, ls_file), os.path.join(path, 'keys.txt'))


def get_and_mod_url(path):
    rename(path)
    mod_urls = list()
    pattern_url = 'https://debank.com/profile/'
    with open(f'{os.path.join(path, "keys.txt")}', 'r') as doc:
        for file in doc.readlines():
            keys = file.replace('\n', '').strip()
            mod_url = f'{pattern_url}{keys}'
            mod_urls.append(mod_url)

    return mod_urls


def get_wallet(url):
    result = list()
    service = Service(f'{os.getcwd()}/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        money_wallet = soup.find('div', attrs={'id': 'root'}).\
            find('div', class_='HeaderInfo_totalAssetInner__1mOQs').get_text().split('-')[0]

        result.append(
            {
                f'{url}': f'{money_wallet}'
            }
        )
        with open(os.path.join(data_folder, 'result.txt'), 'a') as f:
            f.write(f'{url} : {money_wallet}\n')

        print(money_wallet)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    workers = cpu_count()

    futures = []
    length_data = len(get_and_mod_url(path=get_folder))

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        for url in get_and_mod_url(path=get_folder):
            new_future = executor.submit(
                get_wallet,
                url=url
            )
            futures.append(new_future)
            length_data -= 1

    concurrent.futures.wait(futures)


if __name__ == "__main__":
    main()
    shutil.rmtree(get_folder)