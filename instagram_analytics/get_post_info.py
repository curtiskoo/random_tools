from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
import time
from bs4 import BeautifulSoup
import os
from pprint import pprint
import re
from InstagramAPI import InstagramAPI

url = "https://www.instagram.com/eggycouple"
acc = 1
browser = webdriver.Chrome()
browser.get(url)
elems = browser.find_elements_by_xpath("//*[@class='eLAPa']")
elems[0].click()


def key_right(browser):
    actions = ActionChains(browser)
    actions.send_keys(Keys.RIGHT)
    actions.perform()


def get_shortcode(url):
    x = url.split("/")
    ind = x.index('p') + 1
    x = x[ind]
    return x


def get_html_source(html, b=None):
    shortcode = get_shortcode(b)
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find_all("script", {'type': 'text/javascript'})
    temp = list(filter(lambda x: "shortcode_media" in str(x), soup))
    # pprint(temp)
    if len(temp) != 1:
        print("Error at Post: {} | Found shortcode_media: {}".format(acc, len(temp)))
        return
    tt = temp[0].get_text()
    regex = "{(.+?)}"
    find = re.findall(regex, tt)
    find = list(filter(lambda x: shortcode in str(x), find))
    if len(find) != 1:
        print("Error at Post: {} | Found find: {}".format(acc, len(find)))
        print(find)
        return
    find = find[0].replace(":", ",").replace("\"", "").split(",")
    post_id = find[find.index("id") + 1]
    #print(post_id)
    return post_id


def get_url_lst():
    lst_url = []
    right_button = "//a[@class='HBoOv coreSpriteRightPaginationArrow']"
    while True:
        try:
            elem = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, right_button)))
            if browser.current_url not in lst_url:
                lst_url.append(browser.current_url)
            # browser.refresh()
            # html = browser.page_source
            # soup = get_html_source(html)
            key_right(browser)
            # acc += 1
        except TimeoutException:
            print("Done")
            break
    return lst_url

lst_url = get_url_lst()
pprint(lst_url)
print(len(lst_url))

def get_all_id(lst_url):
    lst_id = []
    acc = 1
    for x in lst_url:
        browser.get(x)
        id = get_html_source(browser.page_source, x)
        lst_id.append(id)
        acc += 1
    return lst_id

id_lst = get_all_id(lst_url)

api = InstagramAPI("", "")
api.login()

for x in id_lst:
    api.mediaInfo(x)
    info = api.LastJson
    print(info)