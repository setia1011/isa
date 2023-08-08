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
            title = utils.cleaner(soup.find('article').find('div', class_="jdl__").find('h1').text)
            label = utils.cleaner(soup.find("div", class_="author").text.split("-")[0])
            author = utils.cleaner(soup.find("div", class_="author").text.split("-")[1])
            datetime = utils.cleaner(soup.find("div", class_="date").text)
            contentx = soup.find('article').find("div", class_="detail_text")

            # remove unwanted elements
            for paradetail in contentx.find_all("div", {"class": "paradetail"}):
                paradetail.decompose()
            for multiplebox in contentx.find_all("div", {"class": "multiple-box"}):
                multiplebox.decompose()
            for linksisip in contentx.find_all("table", {"class": "linksisip"}):
                linksisip.decompose()
            for topiksisip in contentx.find_all("table", {"class": "topiksisip"}):
                topiksisip.decompose()
            if contentx.find("div", {"class": "read-full-article"}):
                for u in contentx.find("div", {"class": "read-full-article"}).find_next_siblings():
                    u.decompose()
                for readfullarticle in contentx.find_all("div", {"class": "read-full-article"}):
                    readfullarticle.decompose()
            
            content = utils.cleaner(contentx.text)

            media_article = soup.find('article').find('div', class_='media_artikel')
            if media_article:
                captions = media_article.find_all('div', class_='caption')
                for cap in captions:
                    content += ' ' + utils.cleaner(cap.text)
            
            contents.append({
                'crawled_at': dt.now().strftime('%Y-%m-%d %H:%M:%S'), 
                'label': label, 
                'author': author, 
                'posted_at': datetime, 
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
        
