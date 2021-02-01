from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import datetime
import csv
from os import path

#set up the webdriver that will load the page without opening any browser
#Options for headless so that it doesnt actually open a browser tab
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
#open the page with the webdriver
driver.get('https://www.ladernierechasse.com/')

#wait 20 seconds for the page to load (admittedly a bit clunky, there are better ways)
time.sleep(20)

#get today's date
date = datetime.datetime.now() 

#get the raw html
html = driver.page_source

#quit driver
driver.quit()

#parse it with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")


# #collect the items on the first page as rows
# rows = []
# #find all elements with html tag 'a' (which is the tag for hyperlinks)
# #for which there is an href (which specifies an URL)
# for link in soup.find_all('a', href=True):
#     #specific to "ladernierechasse": STYLE_CODEs are found in the URL
#     #after a llll- and before a ?
#     if 'llll-' in link['href']:
#         result = link['href'].split('llll-')[1]
#         result = result.split("?")[0]
#         rows.append([result])
     
   
#one-liner version of the above code
rows = [[date, link['href'].split('llll-')[1].split("?")[0]] 
        for link in soup.find_all('a', href=True) if 'lll' in link['href'] ]

file_name = 'first_page.csv'
#check if the file already exists or if it's the first time
first_time = not path.exists(file_name)
   
#open a csv to store the data
with open(file_name, 'a', newline='') as file:
    writer = csv.writer(file)
    #if the file is new, write down the columns
    if first_time:
        writer.writerow(["DATE", "STYLE_CODE"])
    #write rows
    for row in rows:
        writer.writerow(row)

