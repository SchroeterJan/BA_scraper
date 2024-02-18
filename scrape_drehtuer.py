from BA_scraper import *
from bs4 import BeautifulSoup

import time

BA_scrape = BAScraper(confirm=confirm, url=BA_url + search_url)


def close_cookies(scrape):
    scrape.driver.find_element(By.CLASS_NAME, "cc_commands").click()


def search(field, searched):
    field.send_keys(searched)  # insert search term
    field.send_keys(Keys.RETURN)  # start search

def get_next(scrape):
    nav_pane = scrape.find_element(By.XPATH, "//div/section/div/div/div/div/div[@class='result_pager']")
    next = nav_pane.find_element(By.XPATH, "//div/nav/div/div/div[@class='next']")
    scrape.execute_script('window.scrollTo(0,' + str(next.location['y']) + ')')
    return next


close_cookies(scrape=BA_scrape)
search_field = BA_scrape.driver.find_element(By.ID, "id3")
search_field.clear()                                       # löschen von eventuellen Eingaben

search(field=search_field, searched='Bundesministergesetz')
time.sleep(1)

soup = BeautifulSoup(BA_scrape.driver.page_source, features="html.parser")
a = 1

while a!=0:

    try:
        next_ = get_next(scrape=BA_scrape.driver)
    except:
        a = 0
    page_results = BA_scrape.driver.find_elements(
        By.LINK_TEXT,
        'Bekanntmachung einer Entscheidung der Bundesregierung nach § 6b des Bundesministergesetzes')
    b = len(page_results)
    for result_num in range(b):
        page_results = BA_scrape.driver.find_elements(
            By.LINK_TEXT,
            'Bekanntmachung einer Entscheidung der Bundesregierung nach § 6b des Bundesministergesetzes')
        result = page_results[result_num]
        BA_scrape.driver.execute_script('window.scrollTo(0,' + str(result.location['y']) + ')')
        result.click()
        result_elem = BA_scrape.driver.find_element(By.XPATH,
                                                    "//div/section/div/div/div/div/div[@class='publication_container']")
        elementHTML = result_elem.get_attribute('outerHTML')  # gives exact HTML content of the element
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')
        result_text = elementSoup.get_text()
        print(result_text)
        back = BA_scrape.driver.find_element(By.LINK_TEXT, "Zurück zum Suchergebnis")
        back.click()
    next_.click()




a = 1
# a = BA_scrape.driver.find_element(By.XPATH, "//div/section/div/div/div/div/div[@class='container result_container global-search']")


