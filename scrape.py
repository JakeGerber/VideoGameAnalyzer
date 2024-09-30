#https://www.pricecharting.com/game/wii/super-mario-galaxy

#Testing page w/ mario galaxy but all pages have same format.


import requests

from bs4 import BeautifulSoup

import csv

import re


def getLinksForConsole(consoleLink):
    print("Links:")

    r = requests.get('https://www.pricecharting.com/console/nes')

    soup = BeautifulSoup(r.content, 'html5lib')

    
    product_rows = soup.find_all('tr', attrs={'data-product': True})

    # Extract product links
    product_links = []
    for row in product_rows:
        # Find the link in the title cell
        title_link = row.find('td', class_='title').find('a')['href']
        # Find the image link
        image_link = row.find('td', class_='image').find('a')['href']
        
        product_links.append({
            'title_link': title_link,
            'image_link': image_link
        })

    # Output the extracted links
    for links in product_links:
        print(f"Title Link: {links['title_link']}, Image Link: {links['image_link']}")

    
    return product_links


def getGameInformation(link):
    r = requests.get(link)

    soup = BeautifulSoup(r.content, 'html5lib')

    details = {}

    game_name = soup.find('h2').get_text(strip=True).replace(':', '')
    print(game_name)

    #Need to strip out the system when in parenthesis and the details part.
    #Regex?

    game_name = game_name.removesuffix(") Details")

    print(game_name)

    system = ""

    while(game_name[-1] != '('):
        system += game_name[-1]
        game_name = game_name[:-1]
        print(game_name)
        #quit()

    system = system[::-1]
    game_name = game_name[:-2]

    print("Game Name:", game_name)
    print("System Name:", system)


    quit()

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
    
    return details.items()









#https://www.pricecharting.com/game/nes/duck-tales-2
#https://www.pricecharting.com/game/gamecube/super-mario-sunshine
#https://www.pricecharting.com/game/playstation-2/xenosaga-3


#r = requests.get('https://www.pricecharting.com/game/wii/super-mario-galaxy')

#r = requests.get('https://www.pricecharting.com/game/gamecube/super-mario-sunshine')

# check status code for response received
# success code - 200
#print(r)

# print content of request
#print(r.content)


#soup = BeautifulSoup(r.content, 'html.parser')
#print(soup.prettify())


#soup = BeautifulSoup(r.content, 'html5lib')
 
 
#table = soup.find('div', attrs = {'id':'full_details'}) 

#for row in table.findAll('td'):
#    print(row)

#print(table)

'''
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


#for key, value in details.items():
#    print(f"{key} : {value}")

'''

#--------------------------------------------------------


'''
#Time to get all Links

r = requests.get('https://www.pricecharting.com/console/nes')

soup = BeautifulSoup(r.content, 'html5lib')

product_rows = soup.find_all('tr', attrs={'data-product': True})

# Extract product links
product_links = []
for row in product_rows:
    # Find the link in the title cell
    title_link = row.find('td', class_='title').find('a')['href']
    # Find the image link
    image_link = row.find('td', class_='image').find('a')['href']
    
    product_links.append({
        'title_link': title_link,
        'image_link': image_link
    })

# Output the extracted links
for links in product_links:
    print(f"Title Link: {links['title_link']}, Image Link: {links['image_link']}")

'''

NES_links = getLinksForConsole(r'https://www.pricecharting.com/console/nes')


allInformation_NES = []

file1 = open(r"C:\Users\Jake\Desktop\Price Checker\Github-Repo\VideoGameAnalyzer\myfile.txt", "w")


for l in NES_links:
    details = getGameInformation(l["image_link"])

    for k, v in details:
        file1.write(k + " : " + v + "\n")
    print("WOW")
    file1.write(r"---------------------------------------------\n\n")
    #break


file1.close()
    




