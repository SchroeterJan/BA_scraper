from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

DEBUG = 0

BA_url = 'https://www.bundesanzeiger.de/'  # Hauptseite des Bundes Anzeiger
search_url = 'pub/de/start?0'             # url zur Suche

confirm = 'Bundesanzeiger'               # Anzeigename bei Verbindungsüberprüfung


class BAScraper:
    url = ""
    confirm = ""

    def __init__(self, url, confirm):
        if DEBUG:  # test for error in Selenium Connection
            print('Connecting Selenium Scraper')
            self.test()
            print('Selenium Scraper is ready')
        self.driver = webdriver.Firefox()  # start driver
        self.url = url
        self.confirm = confirm
        self.connect()  # connect to given URL
        print('Selenium Scraper connected to ' + self.url)

    def test(self):  # test taken from https://selenium-python.readthedocs.io/getting-started.html
        self.driver = webdriver.Firefox()
        driver = self.driver
        driver.get("http://www.python.org")
        assert "Python" in driver.title
        elem = driver.find_element(By.NAME, "q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        self.teardown()

    def connect(self):
        self.driver.get(url=self.url)
        assert self.confirm in self.driver.title

    def teardown(self):
        self.driver.close()
