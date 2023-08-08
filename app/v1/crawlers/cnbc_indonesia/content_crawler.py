import time
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
from app.utils import utils
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.core.config import settings
from app.models import Urls, Contents
import re


def content_crawler(db: Session = Depends):
    try:
        start_time = dt.now()
        print('\n2. Crawling contents...\n===')
        print('Start: {}'.format(start_time))

        chromedriver = settings.ROOT_PATH + "/app/v1/crawlers/chromedriver.exe"
        service = Service(chromedriver)
        options = Options()
        options.add_argument('--incognito')
        options.add_argument('start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(service=service, options=options)

        contents = []
        urls = []

        record = db.query(Urls).filter(Urls.status == 'N').distinct(Urls.url).all()
      
        for i in record:
            driver.get(i.url)
            html = driver.page_source
            soup = bs(html, features='html.parser')

            title = ''
            label = ''
            author = ''
            posted_at = ''
            content = ''

            i0 = soup.find('section', id='content')
            if i0:
                i01 = i0.find('div', class_='l_content')
                if i01:
                    i02 = i01.find('div', class_='content_detail')
                    if i02:
                        ititle = i02.find('h1', class_='title')
                        if ititle:
                            title = utils.cleaner(ititle.get_text())
                        ilabel = i02.find('div', class_='author')
                        if ilabel:
                            label = utils.cleaner(ilabel.get_text())
                            author = utils.cleaner(ilabel.get_text())
                        idate = i02.find('div', class_='date')
                        if idate:
                            posted_at = utils.cleaner(idate.get_text())     
            
                        # get contents
                        j0 = i02.find('div', class_='detail_wrap')
                        if j0:
                            j01 = j0.find('div', class_='detail_text')
                            if j01:
                                # remove unwanted elements
                                paradetailx = j01.find_all("div", {"class": "paradetail"})
                                if paradetailx:
                                    for paradetail in j01.find_all("div", {"class": "paradetail"}):
                                        paradetail.decompose()
                                multipleboxx = j01.find_all("div", {"class": "multiple-box"})
                                if multipleboxx:
                                    for multiplebox in j01.find_all("div", {"class": "multiple-box"}):
                                        multiplebox.decompose() 
                                linksisipx = j01.find_all("table", {"class": "linksisip"})
                                if linksisipx:
                                    for linksisip in j01.find_all("table", {"class": "linksisip"}):
                                        linksisip.decompose()
                                topiksisipx = j01.find_all("table", {"class": "topiksisip"})
                                if topiksisipx:
                                    for topiksisip in j01.find_all("table", {"class": "topiksisip"}):
                                        topiksisip.decompose()
                                if j01.find("div", {"class": "read-full-article"}):
                                    for u in j01.find("div", {"class": "read-full-article"}).find_next_siblings():
                                        u.decompose()
                                    for readfullarticle in j01.find_all("div", {"class": "read-full-article"}):
                                        readfullarticle.decompose()

                                content = utils.cleaner(j01.text)

                                if content:
                                    contents.append({
                                        'crawled_at': dt.now().strftime('%Y-%m-%d %H:%M:%S'), 
                                        'label': label, 
                                        'author': author, 
                                        'posted_at': posted_at, 
                                        'title': title, 
                                        'content': content, 
                                        'url_id': i.id, 
                                        'source_id': i.source_id
                                    })

                                    urls.append({'id': i.id, 'status': 'Y'})
            time.sleep(4)
        
        driver.close()
        db.bulk_insert_mappings(Contents, contents)
        db.bulk_update_mappings(Urls, urls)
        db.commit()
        print('End: {}'.format(dt.now()))
        print('Duration: {}'.format(dt.now() - start_time))
    except Exception as e:
        db.rollback()
        raise
        
