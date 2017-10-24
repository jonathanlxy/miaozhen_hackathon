from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import json

class Selenium_helper:
    def __init__(self, cfg_file=None):
        capa = DesiredCapabilities.CHROME
        capa['pageLoadStrategy'] = 'none'

        # Defind Capabilities with header and load strategy
        if cfg_file:
            self.config = json.load(open(cfg_file, 'rb'))
            capa['chrome.page.settings.userAgent'] = self.config['User_Agent']
        # initiate selenium webdriver, you might need to use webdriver.Chrome('/path/to/chromedriver.exe', desired_capabilities=capa)
        self.driver = webdriver.Chrome(
            self.config['driver_path'],
            desired_capabilities=capa)

    def get(self, url):
        self.driver.get(url)

    def get_tab(self, url):
        #open tab
        # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        self.get('data:,')
        self.get(url)

    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    a = Selenium_helper('selenium_config.json')
    a.get('http://www.google.com')
    score = input('google\n')
    a.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    a.get('http://www.baidu.com')
    score2 = input('baidu\n')
    print(score, score2)
    a.close()