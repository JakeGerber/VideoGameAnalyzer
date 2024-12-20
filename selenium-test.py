from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

import requests

from bs4 import BeautifulSoup

import csv

import re

import os

import json


def getLinksForConsole(consoleLink, getAllLinks=True):
    print("Links:")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(consoleLink)


    # Function to scroll to the bottom of the page
    def scroll_to_bottom(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content to load
            time.sleep(2)  # Adjust the sleep time as needed

            # Calculate new scroll height and compare with last height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    # Scroll to the bottom of the page
    if getAllLinks:
        scroll_to_bottom(driver)

    # Get the page HTML
    html = driver.page_source

    # Print the HTML or save it to a file
    print(html)

    # Close the browser
    driver.quit()


    #r = requests.get(link)

    soup = BeautifulSoup(html, 'html5lib')

    
    product_rows = soup.find_all('tr', attrs={'data-product': True})

    # Extract product links
    product_links = []
    for row in product_rows:
        # Find the link in the title cell
        title_link = row.find('td', class_='title').find('a')['href']
        # Find the image link
        #image_link = row.find('td', class_='image').find('a')['href']
        
        '''
        product_links.append({
            'title_link': title_link,
            'image_link': image_link
        })
        '''
        link = "https://www.pricecharting.com" + title_link
        product_links.append(link)
        

    # Output the extracted links
    for link in product_links:
        print("LINK: ", link)

    #for links in product_links:
    #    print(f"Title Link: {links['title_link']}, Image Link: {links['image_link']}")


    
    return product_links


def getGameInformation(link, details, downloadCoverArtFolder):

    response = requests.get(link)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    print("SOUP: ", soup)

    # Extract the game title
    title = soup.find('h1', class_='chart_title').text.strip()

    title = title.split(" ")

    gameConsole = title[-1].strip()

    title = title[:-1]
    title = " ".join(title).strip()
    
    #Stores all details
    #Format {game : {info}}


    # Print the game title
    print("Title:", title)
    print("Game Console:", gameConsole)

    details[title] = {}
    details[title]["Game Console"] = gameConsole


    coverImageLink = soup.find(class_='cover').find('img')['src'].strip()
    print(coverImageLink)

    #Now need to download Locally


    if not os.path.exists(downloadCoverArtFolder):
        os.makedirs(downloadCoverArtFolder)


    imgDownload = requests.get(coverImageLink)
    
    # Check if the request was successful
    if imgDownload.status_code == 200:
        # Get the image file name from the URL

        newTitle = ""

        for c in title:
            if (c == " " or c.isalnum() == False):
                newTitle += "_"
            elif (c.isalnum()):
                newTitle += c


        img_name = newTitle + "." + coverImageLink.split(".")[-1]
        img_path = os.path.join(downloadCoverArtFolder, img_name)

        newPath = ""
        

        details[title]["Cover Link"] = img_path


        print("path:", img_path)
        
        # Write the image content to a file
        with open(img_path, 'wb') as file:
            file.write(imgDownload.content)
        print(f"Image downloaded and saved as {img_path}")
    else:
        print("Failed to download the image.")


    table = soup.find('table', id='attribute')

    for row in table.find_all('tr'):
        title_cell = row.find('td', class_='title')
        details_cell = row.find('td', class_='details')
        
        if title_cell and details_cell:
            titleC = title_cell.get_text(strip=True).replace(':', '')
            print("----")
            print(title_cell)
            print("******")
            print(details_cell)
            #details[title] = details_cell.get_text(strip=True)
            details[title][titleC] = details_cell.get_text(strip=True)
        else:
            if title_cell:
                print("Not relevant information: ", title_cell)
            if details_cell:
                print("Not relevant information: ", details_cell)



    #quit()

    '''
    # Extract and store the product name in the details dictionary
    if product_name_tag:
        details['product_name'] = product_name_tag.get_text(strip=True)
    else:
        details['product_name'] = "Product name not found."

    # Print the details dictionary
    print(details)

    exit()

    # Find the title inside the "game-page" and "product name" elements
    title = soup.find('div', class_='game-page').find('h1', class_='product-name').text.strip()

    print(title)



    #Need to strip out the console when in parenthesis and the details part.
    #Regex?

    game_name = game_name.removesuffix(") Details")

    #print(game_name)

    console = ""

    while(game_name[-1] != '('):
        console += game_name[-1]
        game_name = game_name[:-1]
        print(game_name)
        #quit()

    console = console[::-1]
    game_name = game_name[:-2]

    #print("Game Name:", game_name)
    #print("System Name:", console)

    details["Game Name"] = game_name
    details["Console"] = console

    #quit()

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


    cover_div = soup.find('div', class_='cover')
    img = cover_div.find('img')

    # Print the image source link
    print(img['src'])


    for key, value in details.items():
        print(f"{key} : {value}")
    '''
    return details
    



# weird edge case
# https://www.pricecharting.com/game/playstation/big-ol%27-bass-greatest-hits?q=big+ol+bass+greatest+hits#used-prices
# add detection for this


NES_links = getLinksForConsole(r'https://www.pricecharting.com/console/nes', getAllLinks=True)

file_name = "NES_Information.json"

allDetails = {}

for gameLink in NES_links:
    details = getGameInformation(gameLink, allDetails, "NES")
    
with open(file_name, "w") as file:
    json.dump(allDetails, file, indent=4)




PS1_links = getLinksForConsole(r'https://www.pricecharting.com/console/playstation', getAllLinks=True)

file_name = "PS1_Information.json"

allDetails = {}

for gameLink in PS1_links:
    details = getGameInformation(gameLink, allDetails, "PS1")
    
with open(file_name, "w") as file:
    json.dump(allDetails, file, indent=4)
