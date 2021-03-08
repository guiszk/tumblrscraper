import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

tags = [ #add your tags here
    'adventure-time',
    'regular-show',
    'steven-universe',
]

def get(tag):
    options = webdriver.ChromeOptions();
    options.add_argument('headless');
    browser = webdriver.Chrome(options=options)

    url = 'https://www.tumblr.com/tagged/' + tag
    browser.get(url)
    time.sleep(1)

    elem = browser.find_element_by_tag_name('body')

    no_of_pagedowns = 2000 #retrieves approx. 2000 lines, depending on the tag
    initial = no_of_pagedowns

    t = time.time()

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        no_of_pagedowns-=1
        td = int(time.time() - t)
        print('[' + tag + '] (' + str(datetime.timedelta(seconds=td)) + ') ' + str(100-int((100*no_of_pagedowns)/initial)) + '%', end='\r')

    print()
    post_elems = browser.find_elements_by_tag_name('p')
    f = open(tag + '.txt', 'w')

    for post in post_elems:
        if(post.text):
            f.write(post.text)
            f.write('\n')
    f.close()
    browser.quit()
    time.sleep(10)
for tag in tags:
    get(tag)
