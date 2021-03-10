import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup as bs

import pandas as pd

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

    no_of_pagedowns = 3000 #retrieves approx. 2000 lines, depending on the tag
    #no_of_pagedowns = 10
    initial = no_of_pagedowns

    t = time.time()

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        no_of_pagedowns-=1
        td = int(time.time() - t)
        print('[' + tag + '] (' + str(datetime.timedelta(seconds=td)) + ') ' + str(100-int((100*no_of_pagedowns)/initial)) + '%', end='\r')

    print()
    post_elems = browser.find_elements_by_tag_name('article')

    for post in post_elems:
        soup = bs(post.get_attribute('innerHTML'), 'html.parser')
        print()
        p = soup.find('p')
        if(p):
            psplit = post.text.split('\n')
            psplit.remove('Follow')
            pdict = {
                'user': pd.Categorical(psplit[0]),
                'text': pd.Categorical(''.join(psplit[1:-2])),
                'tags': pd.Categorical(', '.join(psplit[-2].split('#')[1:])),
                'notes': pd.Categorical(int(psplit[-1].split()[0]))
            }
            df = pd.DataFrame(pdict)
            print(pdict)
            df.to_csv(tag + '.csv', mode='a', index=False)
    browser.quit()
    time.sleep(10)
for tag in tags:
    get(tag)
