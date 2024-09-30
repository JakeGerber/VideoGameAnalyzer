#https://www.pricecharting.com/game/wii/super-mario-galaxy

#Testing page w/ mario galaxy but all pages have same format.


import requests

from bs4 import BeautifulSoup

import csv

#https://www.pricecharting.com/game/nes/duck-tales-2
#https://www.pricecharting.com/game/gamecube/super-mario-sunshine
#https://www.pricecharting.com/game/playstation-2/xenosaga-3


#r = requests.get('https://www.pricecharting.com/game/wii/super-mario-galaxy')

r = requests.get('https://www.pricecharting.com/game/gamecube/super-mario-sunshine')

# check status code for response received
# success code - 200
#print(r)

# print content of request
#print(r.content)


#soup = BeautifulSoup(r.content, 'html.parser')
#print(soup.prettify())


soup = BeautifulSoup(r.content, 'html5lib')
 
 
#table = soup.find('div', attrs = {'id':'full_details'}) 

#for row in table.findAll('td'):
#    print(row)

#print(table)


details = {}

table = soup.find('table', id='attribute')

for row in table.find_all('tr'):
    title_cell = row.find('td', class_='title')
    details_cell = row.find('td', class_='details')
    
    if title_cell and details_cell:
        title = title_cell.get_text(strip=True).replace(':', '')
        details[title] = details_cell.get_text(strip=True)
    else:
        if title_cell:
            print("Not relevant information: ", title_cell)
        if details_cell:
            print("Not relevant information: ", details_cell)


for key, value in details.items():
    print(f"{key} : {value}")
