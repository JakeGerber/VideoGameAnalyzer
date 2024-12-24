import os
from rapidfuzz import fuzz, process
import json


folder_path = 'NES'

#Gets and prints all files in folder
'''
def get_files_in_folder(folder):
    try:
        files = os.listdir(folder)
        result = []

        for file in files:
            if os.path.isfile(os.path.join(folder, file)):
                fileSplit = file.split("|")
                fileName = fileSplit[0]
                fileConsole = fileSplit[1]
                result.append(fileName.replace('_', ' ')+"|"+fileConsole)
                print(result)
        
        return result


        #return [file for file in files if os.path.isfile(os.path.join(folder, file))]
    except Exception as e:
        print(f"Error reading folder: {e}")
        return []
'''

def get_json_names(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    #game_titles = list(data.keys())
    game_titles = list(data.keys())

    #print("Game Titles:")
    #print(game_titles)
    return game_titles


    
def fuzzy_search(files, test_string, threshold=70):
    #Match test_string with each file using fuzz.partial_ratio
    matches = process.extract(
        query=test_string,
        choices=files,
        scorer=fuzz.partial_ratio,
        score_cutoff=threshold  #Only return matches above this threshold
    )
    return matches


def search(game, console, topN=None):


    #This is inefficient to do everytime. I should cache this later so its only done once.
    #files = get_json_names("combined.json")

    files = get_json_names(f"./Game-JSONs/{console}_Information.json")

    gameTitles = set()
    gameConsoles = set()

    for f in files:
        f = f.split("|")
        gameTitles.add(f[0])
        gameConsoles.add(f[1])


    print("game: ", game)


    matches = fuzzy_search(gameTitles, game)
    print("Fuzzy Matches:", matches)

    #What about special editions and such?
    #has issues with not for resale versions (such as doing mario party 2 throws out the not for resale version)
    #fuzzy search is saying that mario party and mario party 2 are 100% on the search.


    if len(matches) > 0:
        print("Matches Found")

        print("Matches Are: ", matches)
        
        returnMatches = []

        matchesAdded = 0
        for match in matches:
            if (topN != None and matchesAdded < topN):
                print(match[0] + "|" + console)
                returnMatches.append(match[0] + "|" + console)
                matchesAdded += 1
            else:
                break
        
        return returnMatches
        #return matches[0][0]+ "|" + console
    else:
        print("ERROR: No matches found. Take a better photo(?)")
        return None


