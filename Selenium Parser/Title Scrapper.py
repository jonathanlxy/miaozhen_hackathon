import re as re
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# defind Capabilities with header and load strategy
capa = DesiredCapabilities.CHROME
capa['pageLoadStrategy'] = 'none'
capa['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'
# initiate selenium webdriver, you might need to use webdriver.Chrome('/path/to/chromedriver.exe', desired_capabilities=capa)
driver = webdriver.Chrome(desired_capabilities=capa)


# parser function
def title_parser(url):
    driver.get('data:,')
    driver.get(url)
    # parse title
    title = driver.title
    n = 0
    # check if chinese characters appear, if nah stop loading after 5 secs
    while re.findall('[\u4e00-\u9fff]+', title) == []:
        time.sleep(.1)
        n += .1
        title = driver.title
        if n > 5:
            break
    # stop loading
    driver.execute_script("window.stop();")

    return title

#load url list
url_list = open('url.csv', 'r').read().split('\n')

# parse title
start = time.time()
title_list = list(map(title_parser, url_list))
end = time.time()
print(end - start)


with open("title.txt", "w") as output:
    for title in title_list:
        output.write(str(title) + '\n')
