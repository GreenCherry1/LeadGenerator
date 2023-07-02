from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import openpyxl
from lxml import html
import requests
import json

def find_all(a, sub):
    start = 0
    out=[]
    while True:
        start = a.find(sub,start)
        if start == -1: break
        out+=[start]
        start += len(sub)
    return out
def Scroll():
    scroll=driver.find_elements(By.CLASS_NAME, 'hfpxzc')[-1]
    scroll_origin=ScrollOrigin.from_element(scroll, 0, 0)
    ActionChains(driver)\
            .move_to_element(scroll)\
            .scroll_from_origin(scroll_origin,0,100)\
            .perform()

def CloseTab():
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    
def ParseHTML(url):
    return driver.page_source
j = {
    "Place": "Дніпровський район",
    "KeyWords": ("Бар", "Кафе"),
    "Amount":10
}
with open("settings.json", "w") as write_file:
    json.dump(j, write_file)

with open("settings.json") as jsonfile:
    data = json.load(jsonfile)
    k = list(data["KeyWords"])
    for i in range(len(k)):
        k[i] = '+'.join(k[i].split())
    a = '+'.join(data["Place"].split())+'+'+'+'.join(k)
    Least_Leads=data["Amount"]
    
def GetEmail(Websites,Website):
    website_index=0
    while website_index<len(Websites):
        print('a')
        resp=ParseHTML(Websites[website_index])
        email=GetEmails_text(resp)
        #if len(email): return email
        print(website_index,len(Websites)-1)
        if website_index==len(Websites)-1:
            print('b')
            Websites=ExpandWebsiteList(Websites,Website,resp)
        website_index+=1
def GetEmails_text(s):
    possible="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789."
    length=len(s)
    out=[]
    for i in range(length):
        if s[i]=='@':
            low,top=i-1,i+1
            for l in range(i-1,0,-1):
                if s[l] not in possible:
                    low=l+1
                    break
            for t in range(i+1,length):
                if s[t] not in possible:
                    top=t
                    break
            out+=[s[low:top]]
    return out

def FindAll_hrefs(url,ParsedHTML):
    all_hrefs_start=find_all(ParsedHTML,'href')
    if not len(all_hrefs_start):return []
    all_hrefs_end=[ParsedHTML.find('"',href) for href in all_hrefs_start]
    all_hrefs=[ParsedHTML[all_hrefs_start[i]+6,all_hrefs_end[i]] for i in range(len(all_hrefs_end))]
    return [website+href for href in all_hrefs if 'http' not in href]
def ExpandWebsiteList(websites,website,resp):
    for web in websites:
        print(FindAll_hrefs(website,resp))
        websites=list(set(websites+FindAll_hrefs(website,resp)))
    return websites

def GetEmail_page(page):
    driver.execute_script("window.open('%s', '_blank')" % page)
    driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[-1])
    emails_links=[i.get_attribute('href') for i in driver.find_elements(By.TAG_NAME,'a') if i and 'mailto' in i.get_attribute('href')]
    if len(emails_links):return emails_links[0]
    
def LogIn_Facebook():
    driver.execute_script("window.open('%s', '_blank')" % "facebook.com")
    driver.implicitly_wait(16)
    driver.switch_to.window(driver.window_handles[-1])
    email_input=driver.find_element(By.XPATH,"//input[@type='email']")
    password_input=driver.find_element(By.XPATH,"//input[@type='password']")
    email_input.send_keys("lmvkd2008@gmail.com")
    password_input.send_keys("#9sbTFm//$3#G4i\n")
    CloseTab()
def GetEmail_Facebook():
    pics=driver.find_elements(By.XPATH,"//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h']")
    for i in pics:
        if '@' in i.text:
            print("a")
            return i.text
    return ''
driver = webdriver.Chrome()
driver.get("https://kalaki.eatbu.com/?lang=uk#contact")
print(GetEmail(["https://kalaki.eatbu.com/"],"https://kalaki.eatbu.com/"))
print(ParseHTML("https://kalaki.eatbu.com/?lang=uk#contact"))
'''
wb=openpyxl.load_workbook("output.xlsx")
ws=wb.active
driver = webdriver.Chrome()
driver.get("https://www.google.com.ua/maps/search/"+a+'?hl=en')
Full_Leads=0
links,used_links=[],[]

while Full_Leads<Least_Leads:
    Scroll()
    used_links+=[i[:i.find('data')] for i in links]
    links = [i.get_attribute('href')for i in driver.find_elements(By.CLASS_NAME, 'hfpxzc') if i.get_attribute('href')[:i.get_attribute('href').find('data')] not in used_links]
    if not len(links):break
    for i in links:
        driver.execute_script("window.open('%s', '_blank')" % i)
        driver.implicitly_wait(10)
        driver.switch_to.window(driver.window_handles[-1])
        add= [x.text for x in driver.find_elements(By.CLASS_NAME, 'DkEaL')]
        pictures_buttons=driver.find_elements(By.CLASS_NAME, 'CsEnBe')
        pictures_aria_label=[x.get_attribute("aria-label") for x in pictures_buttons]
        pictures_links=list(set([x.get_attribute('href') for x in pictures_buttons if x.tag_name=='a' and x.get_attribute('aria-label')!='Claim this business']))
        
        if not len(pictures_links):
            CloseTab()
            continue
        ws.cell(row = Full_Leads+2, column = 2).value=' '.join(pictures_links)
        HasPhone=False
        for pic in pictures_aria_label:
            if "Plus code" in pic:ws.cell(row = Full_Leads+2, column = 1).value=pic[11:]
            if "Phone" in pic:
                ws.cell(row = Full_Leads+2, column = 3).value=pic[6:]
                HasPhone=True
        GetEmail(pictures_links)
        if(Full_Leads==Least_Leads):break
wb.save("output.xlsx")
driver.quit()
'''
