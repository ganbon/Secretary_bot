from copy import copy
from moodle.config import *
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import re
import unicodedata
def moodel_data():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path = driver_path, chrome_options = options)
    driver.get('https://kadai-moodle.kagawa-u.ac.jp/login/index.php') #moodleのログインurl
    login_id = driver.find_element_by_id("username")
    login_id.send_keys(USER)
    login_password = driver.find_element_by_id("password")
    login_password.send_keys(PASS)
    login_btn = driver.find_element_by_id("loginbtn")
    login_btn.click()
    driver.get('https://kadai-moodle.kagawa-u.ac.jp/calendar/view.php?view=month') #moodelのカレンダ-url
    html1 = driver.page_source
    next_month = driver.find_element_by_class_name('arrow_link.next')
    url = next_month.get_attribute("href")
    driver.get(url)
    html2 = driver.page_source
    driver.close()
    return html1,html2

def extract_html(html):
    plan_data = []
    date = []
    mat = [] 
    now_date = datetime.now()
    day = int(now_date.day)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    r = []
    thread = table.find('thead')
    ths = thread.tr.find_all('th')
    for th in ths:
        r.append(th.text)
    mat.append(r)
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:
        r = []
        for td in tr.find_all('td'):
            r.append(td.text)
        mat.append(r)
    num_text = ''
    for r in mat:
        text = ','.join(r)
        text = text.replace('\n',',')
        text = text.replace(' ','.')
        text = text.replace(u'\xa0','')
        text = text.replace(u'\u3000','')
        num_text += text
        text_list = list(dict.fromkeys(num_text.split(',')))
    for data in text_list:
        if 'イベントなし' in data:
            continue
        elif '2022年' in data:
            date = []
            date = data.split('.')[2:]
            date = [int(re.sub(r"\D", "", x)) for x in date]
            if date[2] < day:
                continue 
            date += [None,None]
        elif date != [] and len(set(data)) > 3:
            d = copy(date)
            data = data.replace('.',' ')
            re_data = re.search(r'「.*?」',data)
            if re_data:
                context = re_data.group()
                context = unicodedata.normalize('NFKC', context)
                d.append(context)
            else:
                d.append(data)
            plan_data.append(d)
    return plan_data