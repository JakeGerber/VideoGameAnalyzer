from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import os
import json

#potentially add regex at some point?
import re

def getLinksForConsole(consoleLink, getAllLinks=True):
    print("Links:")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(consoleLink)

    #Scrolls to the bottom of the page.
    def scroll_to_bottom(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            #Scroll to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #Wait for new content to load
            time.sleep(2)

            #Calculate new scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    #If getAllLinks is true, scroll to the bottom of the page.
    if getAllLinks:
        scroll_to_bottom(driver)

    #Get the page html
    html = driver.page_source
    
    #print(html)

    #Close the browser
    driver.quit()

    soup = BeautifulSoup(html, 'html5lib')
    product_rows = soup.find_all('tr', attrs={'data-product': True})

    #Extract product links
    product_links = []
    for row in product_rows:
        #Find the link in the title cell
        title_link = row.find('td', class_='title').find('a')['href']
        #Find the image link
        link = "https://www.pricecharting.com" + title_link
        product_links.append(link)
        

    #Printing out links.
    for link in product_links:
        print("LINK: ", link)

    return product_links


def getGameInformation(link, details, downloadCoverArtFolder):

    response = requests.get(link)

    #Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    if soup == None:
        print("ERROR WITH: ", link, " - moving on")
        return

    #Get game title and console.
    title = soup.find('h1', class_='chart_title').text.strip()
    title = title.split(" ")
    gameConsole = title[-1].strip()
    title = title[:-1]
    title = " ".join(title).strip()

    print("Title:", title)
    print("Game Console:", gameConsole)

    coverImageLink = soup.find(class_='cover').find('img')['src'].strip()
    print("Game Cover Link:",coverImageLink)

    if (coverImageLink == f"/images/no-image-available.png"):
        return

    #eventually title should be replaced with the ID of the game
    details[title] = {}
    details[title]["title"] = title
    details[title]["game-console"] = gameConsole


    #Locally downloads Cover Arts
    if not os.path.exists(downloadCoverArtFolder):
        os.makedirs(downloadCoverArtFolder)

    imgDownload = requests.get(coverImageLink)
    
    #Check if the request was successful
    if imgDownload.status_code == 200:
        
        #When downloading files change spaces and special characters to _
        newTitle = ""

        for c in title:
            if (c == " " or c.isalnum() == False):
                newTitle += "_"
            elif (c.isalnum()):
                newTitle += c

        img_name = newTitle + "." + coverImageLink.split(".")[-1]
        img_path = os.path.join(downloadCoverArtFolder, img_name)

        newPath = ""
        
        details[title]["cover-link"] = img_path


        print("path:", img_path)
        
        #Write the image content to a file
        with open(img_path, 'wb') as file:
            file.write(imgDownload.content)
        print(f"Image downloaded and saved as {img_path}")
    else:
        print("Failed to download the image.")


    table = soup.find(id="price_data")

    rows = table.find_all("tr")

    price_cells = rows[1].find_all("td")
    details[title]["loose_price"] = price_cells[0].find("span", class_="price").text.strip()
    details[title]["complete_price"] = price_cells[1].find("span", class_="price").text.strip()
    details[title]["new_price"] = price_cells[2].find("span", class_="price").text.strip()
    details[title]["graded_price"] = price_cells[3].find("span", class_="price").text.strip()
    details[title]["box_only_price"] = price_cells[4].find("span", class_="price").text.strip()
    details[title]["manual_only_price"] = price_cells[5].find("span", class_="price").text.strip()


    table = soup.find('table', id='attribute')

    for row in table.find_all('tr'):
        title_cell = row.find('td', class_='title')
        details_cell = row.find('td', class_='details')
        
        if title_cell and details_cell:
            titleC = title_cell.get_text(strip=True).replace(':', '').lower().replace(" ", "-").replace("-", "_")
            
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

    return details
    



# Added detection for weird cases like this
# https://www.pricecharting.com/game/playstation/big-ol%27-bass-greatest-hits?q=big+ol+bass+greatest+hits#used-prices


NES_links = getLinksForConsole(r'https://www.pricecharting.com/console/nes', getAllLinks=True)

#NES_links = [f"https://www.pricecharting.com/game/nes/commando-5-screw"]

file_name = "NES_Information.json"

allDetails = {}

for gameLink in NES_links:
    details = getGameInformation(gameLink, allDetails, "NES")
    
with open(file_name, "w") as file:
    json.dump(allDetails, file, indent=4)


'''
PS1_links = getLinksForConsole(r'https://www.pricecharting.com/console/playstation', getAllLinks=True)

file_name = "PS1_Information.json"

allDetails = {}

for gameLink in PS1_links:
    details = getGameInformation(gameLink, allDetails, "PS1")
    
with open(file_name, "w") as file:
    json.dump(allDetails, file, indent=4)
'''

#Nintendo (Home Consoles):
# nes, super-nintendo, nintendo-64, gamecube, wii, wii-u, nintendo-switch

#Nintendo (Handhelds):
# gameboy, gameboy-color, gameboy-advance, nintendo-ds, nintendo-3ds, virtual-boy, game-&-watch


#Playstation (Home Consoles)
# playstation, playstation-2, playstation-3, playstation-4, playstation-5

#Playstation (Handhelds):
# psp, playstation-vita