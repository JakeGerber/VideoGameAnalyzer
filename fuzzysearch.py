import os
from rapidfuzz import fuzz, process
import json


folder_path = 'NES'

#Gets and prints all files in folder
def get_files_in_folder(folder):
    try:
        files = os.listdir(folder)
        result = []

        for file in files:
            if os.path.isfile(os.path.join(folder, file)):
                result.append(file.replace('_', ' '))
        
        return result


        #return [file for file in files if os.path.isfile(os.path.join(folder, file))]
    except Exception as e:
        print(f"Error reading folder: {e}")
        return []
    

def get_json_names(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    #game_titles = list(data.keys())
    game_titles = list(data.keys())

    print("Game Titles:")
    print(game_titles)
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


def search(game, console):
    #files = get_files_in_folder(folder_path)

    #print("Files:", files)


    #test = "Galaga Demons of Death"

    files = get_json_names("NES_Information.json")

    matches = fuzzy_search(files, game)
    print("Fuzzy Matches:", matches)

    #What about special editions and such?
    if len(matches) > 0:
        print("Matches Found")
        return matches[0][0]
    else:
        print("ERROR: No matches found. Take a better photo(?)")
        return None
