from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support.wait import WebDriverWait
import openpyxl
import requests
import json

class Scraper:
    def __init__(self):
        return self.driver = webdriver.Chrome()
	
    def scroll(self, driver):
        """
        Perform scrolling action on the web page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        scroll = driver.find_elements(By.CLASS_NAME, 'hfpxzc')[-1]
        scroll_origin = ScrollOrigin.from_element(scroll, 0, 0)
        ActionChains(driver) \
            .move_to_element(scroll) \
            .scroll_from_origin(scroll_origin, 0, 100) \
            .perform()

    def close_tab(self, driver):
        """
        Close the current tab and switch to the last tab.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])

    def get_email_page(self, driver, pages, HasPhone):
        """
        Extract email addresses from web pages.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            pages (list): List of URLs to visit.
            HasPhone (bool): Flag indicating if phone number is already found.

        Returns:
            dict: Dictionary containing the email and phone number found on the page.
        """
        headers = {'User-Agent': 'Chrome/92.0.4515.107'}
        out = {'phone': '', 'email': ''}
        for page in pages:
            try:
                code = requests.get(page, headers=headers).status_code
            except Exception as ex_:
                print(ex)
                continue
            if code != 200:
                continue
            driver.execute_script("window.open('%s', '_blank')" % page)
            driver.implicitly_wait(10)
            driver.switch_to.window(driver.window_handles[-1])
            links = driver.find_elements(By.TAG_NAME, 'a')
            for i in links:
                try:
                    if "facebook" in i.get_attribute('href'):
                        email = self.get_email_facebook(driver, i.get_attribute('href'))
                        if email:
                            self.close_tab(driver)
                            out['email'] = email
                            if HasPhone:
                                return out
                except Exception as ex_:
                    print(ex_)
                    continue
                try:
                    if not HasPhone and 'tel' in i.get_attribute("href"):
                        out['phone'] = i.get_attribute("href")[4:]
                        if out['email']:
                            self.close_tab(driver)
                            return out
                    if 'mailto' in i.get_attribute("href"):
                        out['email'] = i.get_attribute("href")[7:]
                        if HasPhone or out['phone']:
                            self.close_tab(driver)
                            return out
                except Exception as ex_:
                    print(ex_)
            self.close_tab(driver)
        return out

    def log_in_facebook(self, driver):
        """
        Log in to Facebook.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        email_input = driver.find_elements(By.XPATH, "//input[@type='email']")
        if len(email_input):
            email_input = email_input[0]
        else:
            return
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        email_input.send_keys("lmvkd2008@gmail.com")
        password_input.send_keys("#9sbTFm//$3#G4i\n")

    def get_email_facebook(self, driver, page):
        """
        Extract email address from Facebook page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            page (str): URL of the Facebook page.

        Returns:
            str: The email address found on the page.
        """
        driver.execute_script("window.open('%s', '_blank')" % page)
        driver.implicitly_wait(10)
        driver.switch_to.window(driver.window_handles[-1])
        self.log_in_facebook(driver)
        info = driver.find_elements(By.XPATH,"//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h']")
        for i in info:
            text = i.text
            if '@' in text:
                self.close_tab(driver)
                return text
        self.close_tab(driver)
        return ''
    def run_scraper(self, search, Least_Leads):
        """
        Run the web scraper.

        Args:
            Search (str): The search query.
            Least_Leads (int): The minimum number of leads to be scraped.
        """
        Soc_networking_list = [
            "facebook", "instagram", "glovo", "t.me/", "tiktok", "twitter", "reddit", "tumblr", "flickr", "instagtam"
        ]
        wb = openpyxl.Workbook()
        ws = wb.active
        driver = webdriver.Chrome()
        driver.get("https://www.google.com.ua/maps/search/" + Search + '?hl=en')
        Full_Leads = 0
        links, used_links = [], 0
        while Full_Leads < Least_Leads:
            self.scroll(driver)
            used_links += len(links)
            WebDriverWait(driver, timeout=10).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'hfpxzc')) > used_links
            )
            links = [i.get_attribute('href') for i in driver.find_elements(By.CLASS_NAME, 'hfpxzc')[used_links:]]
            if not len(links):
                print('no more places')
                break
            for i in links:
                driver.execute_script("window.open('%s', '_blank')" % i)
                driver.implicitly_wait(10)
                driver.switch_to.window(driver.window_handles[-1])
                pictures_buttons = driver.find_elements(By.CLASS_NAME, 'CsEnBe')
                pictures_aria_label = [x.get_attribute("aria-label") for x in pictures_buttons]
                websites = list(set([x.get_attribute('href') for x in pictures_buttons if x.tag_name == 'a' and x.get_attribute('aria-label') != 'Claim this business']))
                own_websites = [website for website in websites if sum([int(socnetwork in website) for socnetwork in Soc_networking_list]) == 0 and website[-3:] != 'pdf']
                if not len(websites):
                    self.close_tab(driver)
                    continue
                HasPhone = False
                for pic in pictures_aria_label:
                    if "Plus code" in pic:
                        ws.cell(row=Full_Leads + 1, column=1).value = pic[11:]
                    if "Phone" in pic:
                        ws.cell(row=Full_Leads + 1, column=3).value = pic[6:]
                        HasPhone = True
                email = {'email': '', 'phone': ''}
                if len(own_websites):
                    email = self.get_email_page(driver, own_websites, HasPhone)
                    ws.cell(row=Full_Leads + 1, column=2).value = ' '.join(own_websites)
                else:
                    ws.cell(row=Full_Leads + 2, column=2).value = ' '.join(websites)
                    for website in websites:
                        if 'facebook' in website:
                            email['email'] = self.get_email_facebook(driver, website)
                            break
                if email['phone']:
                    ws.cell(row=Full_Leads + 1, column=3).value = email['phone']
                    HasPhone = True
                if HasPhone and email['email']:
                    ws.cell(row=Full_Leads + 1, column=4).value = email['email']
                    Full_Leads += 1
                print(email)
                self.close_tab(driver)
                if Full_Leads == Least_Leads:
                    break
        wb.save("Leads.xlsx")
        driver.quit()

with open("settings.json") as jsonfile:
    data = json.load(jsonfile)
    k = list(data["KeyWords"])
    for i in range(len(k)):
        k[i] = '+'.join(k[i].split())
    Search = '+'.join(data["Place"].split()) + '+' + '+'.join(k)
    Least_Leads = data["Amount"]
scraper = Scraper()
scraper.run_scraper(Search, Least_Leads)
