from BA_scraper import *
from bs4 import BeautifulSoup
from re_analysis import *
import pandas as pd

import time
import locale

# define locale time format
locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
# create scraper object
BA_scrape = BAScraper(confirm=confirm, url=BA_url + search_url)


def close_cookies(scrape):
    # closes cookie question answering "no"
    scrape.find_element(By.CLASS_NAME, "cc_commands").click()


def search(field, searched):
    field.send_keys(searched)  # insert search term
    field.send_keys(Keys.RETURN)  # start search


def get_next(scrape):
    nav_pane = scrape.find_element(By.XPATH, "//div/section/div/div/div/div/div[@class='result_pager']")
    next_ = nav_pane.find_element(By.XPATH, "//div/nav/div/div/div[@class='next']")
    scrape.execute_script('window.scrollTo(0,' + str(next_.location['y']) + ')')
    return next_


def get_current_page(scrape):
    nav_pane = scrape.find_element(By.XPATH, "//div/section/div/div/div/div/div[@class='result_pager']")
    active = nav_pane.find_element(By.XPATH, "//div/nav/div/div/div/a[@class=' active']")
    scrape.execute_script('window.scrollTo(0,' + str(active.location['y']) + ')')
    return active


def get_results(scraper):
    return scraper.find_elements(
        By.LINK_TEXT,
        'Bekanntmachung einer Entscheidung der Bundesregierung nach § 6b des Bundesministergesetzes')


def open_result(scraper):
    page_results = get_results(scraper=scraper)
    result = page_results[result_num]
    # scrolling down to current result location
    scraper.execute_script('window.scrollTo(0,' + str(result.location['y']) + ')')
    result.click()


def prep_text(text):
    # normalize text to unicode using the most common normal form NFC which is adviced for html

    # replace new line "\n" and carriage return "\r"
    # source for exploring unicode https://unicode-explorer.com
    text = text.replace('\n', ' ').replace('\r', '')
    text = text.replace('\xad', '')
    text = text.replace('\u00ad', '')
    text = text.replace('\u00a0', ' ')  # replacing "no-break space" &nbsp
    text = text.replace('\u2004', ' ')
    text = text.replace('\u2006', ' ')
    text = text.replace('\N{SOFT HYPHEN}', '')
    text = unicodedata.normalize("NFC", text)
    return text


def analyze_text(text, multi_no):
    anrede = get_anrede(text)
    ad = get_ad(text)           # Erkennung des Kürzels für "außer Dienst" aufgrund unterschiedlicher Schreibweise
    funktion = get_funktion(text=text, anrede=anrede, ad=ad)
    name = get_name(text, ad=ad)
    taetigkeit, multi = get_taetigkeit(text, multi_no)
    date_sitzung, empfehlung = get_date_sitzung(text)
    date_bekannt = get_date_bekannt(text, anrede)
    folgend = get_folgend(text, empfehlung)
    beschluss = get_beschluss(text, multi, empfehlung)
    result_list = [anrede, funktion, name, taetigkeit, date_sitzung, date_bekannt, folgend, beschluss]
    if None in result_list:
        a = 1
    return result_list, multi

# closing cookies window that opened after initializing the scraper and landing on the BA website
close_cookies(scrape=BA_scrape.driver)
search_field = BA_scrape.driver.find_element(By.ID, "id3")      # finding search field
search_field.clear()                                            # löschen von eventuellen Eingaben
search(field=search_field, searched='Bundesministergesetz')     # Ausführen der Suche
time.sleep(1)

daten = []
change = True
while change:
    page_results = get_results(scraper=BA_scrape.driver)        # alle Ergebnisse der aktuellen Seite
    for result_num in range(len(page_results)):
        open_result(scraper=BA_scrape.driver)
        result_header = BA_scrape.driver.find_element(By.XPATH,
                                                      "//div/section/div/div/div/div/div/div/div/div[@class='info']")
        headerHTML = (result_header.get_attribute('outerHTML'))  # gives exact HTML content of the element
        headerSoup = BeautifulSoup(headerHTML, 'html.parser')
        header_text = headerSoup.get_text()
        header_text = prep_text(header_text)
        id_ = re_search(pattern=r'BAnz (.+?)  ', text=header_text)
        print(id_)      # print id to track errors more easily
        result_elem = BA_scrape.driver.find_element(By.XPATH,
                                                    "//div/section/div/div/div/div/div[@class='publication_container']")
        resultHTML = result_elem.get_attribute('outerHTML')  # gives exact HTML content of the element
        resultSoup = BeautifulSoup(resultHTML, 'html.parser')
        raw_result_text = resultSoup.get_text()
        result_text = prep_text(text=raw_result_text)
        multi_no = 1
        result_daten, multi = analyze_text(result_text, str(multi_no))
        result_daten.append(id_)
        daten.append(result_daten)
        if multi != 1:
            multi_no += 1
            while multi_no <= multi:
                result_daten, more_multi = analyze_text(result_text, str(multi_no).encode('unicode-escape').decode())
                result_daten.append(id_)
                daten.append(result_daten)
                multi_no += 1
        print(result_num)
        back = BA_scrape.driver.find_element(By.LINK_TEXT, "Zurück zum Suchergebnis")
        back.click()
    current_page = int(get_current_page(scrape=BA_scrape.driver).text)
    next_ = get_next(scrape=BA_scrape.driver)
    next_.click()
    if int(get_current_page(scrape=BA_scrape.driver).text) == current_page:
        change = False

daten_frame = pd.DataFrame(data=daten,columns=['Anrede',
                                    'Funktion',
                                    'Name',
                                    'Tätigkeit_geplant',
                                    'Datum_SitzungBundesregierung',
                                    'Datum_Bekanntmachung',
                                    'Beratungfolgend',
                                    'Entscheidung',
                                    'id'
                                    ])

# a = BA_scrape.driver.find_element(By.XPATH, "//div/section/div/div/div/div/div[@class='container result_container global-search']")
