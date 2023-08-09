import time
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
from app.utils import utils
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.v1.services import install as install_service


def url_crawler(keywords: str, date: str, pages: int, db: Session = Depends):
    try:
        start_time = dt.now()
        print('\n1. Crawling urls...\n===')
        print('Start: {}'.format(start_time))

        chromedriver = settings.ROOT_PATH + "/app/v1/crawlers/chromedriver.exe"
        service = Service(chromedriver)
        options = Options()
        options.add_argument('--incognito')
        options.add_argument('start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(service=service, options=options)

        site_url = "https://www.cnnindonesia.com/search?query={keywords}&date={date}"\
            .format(keywords=utils.url_encode(keywords), date=date)
    
        driver.get(site_url)

        urls = []
        next_page = [site_url]

        if pages:
            for i in range(pages):
                if i < len(next_page):
                    driver.get(next_page[i])
                    html = driver.page_source
                    soup = bs(html, features='html.parser')
                    boxes = soup.find('div', class_='list media_rows middle').find_all('article')

                    for box in boxes:
                        try:
                            url = box.find('a', href=True)['href']
                        except Exception as e:
                            # url = ''
                            pass
                        urls.append({
                            'crawled_at': dt.now().strftime('%Y-%m-%d %H:%M:%S'), 
                            'url': url, 
                            'source_id': 1, 
                            'status': 'new'
                        })

                    # get the next page
                    if len(next_page) < pages:
                        paging = soup.find('div', class_="pagination")
                        if paging:
                            nx = paging.findAll('a', href=True)[-1]['href']
                            if len(nx) > 10:
                                next_page.append('https://www.cnnindonesia.com{p}'.format(p=nx))
                    time.sleep(4)
        
        driver.close()

        for i in urls:
            print(i)
            try:
                q = install_service.insert_url(
                    crawled_at=i['crawled_at'], 
                    url=i['url'], 
                    source_id=i['source_id'], 
                    status=i['status'], 
                    db=db
                )
                db.add(q)
                db.commit()
            except Exception as e:
                db.rollback()
        print('End: {}'.format(dt.now()))
        print('Duration: {}'.format(dt.now() - start_time))
    except Exception as e:
        db.rollback()