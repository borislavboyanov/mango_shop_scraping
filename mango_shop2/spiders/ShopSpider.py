import json
import scrapy
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ShopspiderSpider(scrapy.Spider):
    name = 'ShopSpider'
    allowed_domains = ['shop.mango.com']
    start_urls = ['https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99/']

    def start_requests(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        ser = Service('geckodriver path')
        self.driver = webdriver.Firefox(service=ser, options=options)
        for url in self.start_urls:
            self.driver.get(url)
            # _ = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'selector-list')))
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        name = self.driver.find_element(By.CLASS_NAME, 'product-name').text
        if 'product-sale--discount' in self.driver.page_source:
            price = self.driver.find_element(By.CLASS_NAME, 'product-sale--discount').text
        else:
            price = self.driver.find_element(By.CLASS_NAME, 'product-sale').text
        price = float(price[3:])
        color = self.driver.find_element(By.CLASS_NAME, 'colors-info-name').text
        sizes = []
        elements = self.driver.find_element(By.CLASS_NAME, 'selector-list').find_elements(By.CSS_SELECTOR, '*')
        for element in elements:
            size = element.get_attribute('data-size')
            if size != None:
                sizes.append(size)

        result = {'name': name, 'price': price, 'color': color, 'size': sizes}
        with open('data.txt', 'w') as outfile:
            json.dump(result, outfile)
        self.driver.close()
