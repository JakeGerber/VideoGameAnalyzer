from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import os
import json
import glob

def getLinksForConsole(consoleLink: str, getAllLinks: bool=True) -> list[str]:
    """
    Retrieves a list of links for a given console based on the provided console link.

    Args:
        consoleLink (str): The URL of the console on pricecharting.com which lists all the games.
        getAllLinks (bool): A flag to determine whether to fetch all links (default is True).

    Returns:
        list[str]: A list of strings representing the retrieved links.
    """


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


def getGameInformation(link: str, details: dict[str, str], downloadCoverArtFolder: str, console: str) -> dict[str, str]:
    """
    Gets all details for link passed in (such as title, price, developer, etc).

    Args:
        link (str): The URL of the game on pricecharting.com.
        details (dict[str, str]): The full list of details passed in, which is added to.
        downloadCoverArtFolder (str): The folder where cover art images will be saved.
        console (str): The console of the game that is downloaded.

    Returns:
        dict[str, str]: The full list of details, now added to with this game.
    """

    response = requests.get(link)

    #Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    if soup == None:
        print("ERROR WITH: ", link, " - moving on")
        return

    try:
        #Get game title and console.
        title = soup.find('h1', class_='chart_title').text.strip()
        title = title.split(" ")
        print("CONSOLE: ", console)
        gameConsole = console
        consoleSpaces = len(console.replace("-", " ").split(" "))
        print("CONSOLE SPACES: ", consoleSpaces)
        title = title[:-consoleSpaces]
        title = " ".join(title).strip()

        print("Title:", title)
        print("Game Console:", console)

        coverImageLink = soup.find(class_='cover').find('img')['src'].strip()
        print("Game Cover Link:",coverImageLink)

        #Only use games with cover art images.
        if (coverImageLink == f"/images/no-image-available.png"):
            print("NO IMAGE: ", link, " - moving on")
            return

        #eventually title should be replaced with the ID of the game
        gameTitle = title + "|" + console
        gameTitle = gameTitle.lower()
        details[gameTitle] = {}
        details[gameTitle]["title"] = title
        details[gameTitle]["game-console"] = gameConsole


        #Locally downloads Cover Arts
        #Eventually use database to store (if desired)
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
            
            details[gameTitle]["cover-link"] = img_path

            #Here you would want to connect to s3 database
            #Upload images, and change link


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
        details[gameTitle]["loose_price"] = price_cells[0].find("span", class_="price").text.strip()
        details[gameTitle]["complete_price"] = price_cells[1].find("span", class_="price").text.strip()
        details[gameTitle]["new_price"] = price_cells[2].find("span", class_="price").text.strip()
        details[gameTitle]["graded_price"] = price_cells[3].find("span", class_="price").text.strip()
        details[gameTitle]["box_only_price"] = price_cells[4].find("span", class_="price").text.strip()
        details[gameTitle]["manual_only_price"] = price_cells[5].find("span", class_="price").text.strip()


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
                details[gameTitle][titleC] = details_cell.get_text(strip=True)
            else:
                if title_cell:
                    print("Not relevant information: ", title_cell)
                if details_cell:
                    print("Not relevant information: ", details_cell)
    except Exception as e:
        print(e)

    return details
    


recreate_JSON_if_exists = False

#List of consoles, names are as seen on pricecharting.com
consoles = ["gameboy", "nes", "super-nintendo", "nintendo-64", "wii", "wii-u", "nintendo-switch", "playstation-4", "playstation-5", "xbox-one"]

for console in consoles:

    file_name = f"./Game-JSONs/{console}_Information.json"

    if (os.path.exists(f"./Game-JSONs/{console}_Information.json") and recreate_JSON_if_exists == False):
        print("FILE EXISTS, moving on!")
        continue

    console_links = getLinksForConsole(fr'https://www.pricecharting.com/console/{console}', getAllLinks=True)
    

    allDetails = {}

    for gameLink in console_links:
        details = getGameInformation(gameLink, allDetails, downloadCoverArtFolder=console, console=console)
        
    with open(file_name, "w") as file:
        json.dump(allDetails, file, indent=4)


#Combine everything into one JSON

json_files = glob.glob(f"./Game-JSONs/*.json")

combined_data = {}

for file in json_files:
    with open(file, 'r') as f:
        data = json.load(f)
        combined_data.update(data)

with open("combined.json", "w") as f:
    json.dump(combined_data, f, indent=4)




#Nintendo (Home Consoles):
# nes, super-nintendo, nintendo-64, gamecube, wii, wii-u, nintendo-switch

#Nintendo (Handhelds):
# gameboy, gameboy-color, gameboy-advance, nintendo-ds, nintendo-3ds, virtual-boy, game-&-watch

#Playstation (Home Consoles)
# playstation, playstation-2, playstation-3, playstation-4, playstation-5

#Playstation (Handhelds):
# psp, playstation-vita

#Atari
# atari-2600, atari-5200, atari-7800, atari-400, atari-lynx, atari-jaguar

#Sega
# sega-genesis, sega-master-system, sega-cd, sega-32x, sega-saturn, sega-dreamcast, sega-game-gear, sega-pico

#Xbox
# xbox, xbox-360, xbox-one, xbox-series-x


# Added detection for weird cases like this
# https://www.pricecharting.com/game/playstation/big-ol%27-bass-greatest-hits?q=big+ol+bass+greatest+hits#used-prices
# Only accounts for games released to NA (doesn't support EU or JP)
