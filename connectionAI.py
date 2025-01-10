#https://platform.openai.com/docs/guides/vision
#Need to pass images into OpenAI using base64

#Need to add env for dynamodb database instead of putting it here each time.

'''
Plan!:

-Extract Text from Image using OpenAI LLM
-Fuzzy search on images in S3 bucket to get names
-Use logo detection in corners to find out if its a special version of the game.

'''


'''
SOMETIMES THE RESULT IS LIKE

KEY IS:  ```
The Guardian Legend
```|nes

and i have no idea why this happens?

'''



import base64
import os
from openai import OpenAI
import json
import boto3

from boto3.dynamodb.conditions import Key, Attr

from dotenv import load_dotenv

from rapidfuzz import fuzz, process

import difflib

#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process



#maybe verify result with regex

def json_to_txt(json_path):
    
  with open(json_path, 'r') as file:
    data = json.load(file)

  allKeys = set()
  
  for k in data.keys():
    allKeys.add(k.split("|")[0])

  return '\n'.join(f"{key}\n{key}" for key in allKeys)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def connectToAI(image_path):
  # Path to your image
  #image_path = "IMG_1972.png"

  # Getting the base64 string
  base64_image = encode_image(image_path)

  extension = image_path.split(".")[-1]
  print(extension)

  api_key = os.getenv("OPENAI_API_KEY")
  print(api_key)

  client = OpenAI(
      api_key=api_key
  )


#Changing gpt-4o-mini to gpt-3.5-turbo

  #If i wanted to add support for pictures of multiple games at a time, I would probably ask for format and identify the amount of
  #games in the image and what they are

  #update completion to include more consoles.
  image_url = f"data:image/{extension};base64,{base64_image}"

  completion = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": [
            {
                "type": "text",
                "text": "What console is this on? Your possible choices are nes, super-nintendo, playstation, playstation-2, nintendo-64, wii, wii-u, nintendo-switch, playstation-4, playstation-5, and xbox-one. Only print it out and if it is none of these or unknown, print unknown.",
            },
            {
                "type": "image_url",
                "image_url": {
                  "url": image_url
                },
            },
        ]}
    ]
  )

  #print(completion.choices[0].message.content.strip())

  console = "unknown"
  gameItself = "unknown"

  console = completion.choices[0].message.content.strip()

  #old way with just jsons not using dynamodb
  #allGamesForConsole = json_to_txt(f"./Game-JSONs/{completion.choices[0].message.content.strip()}_Information.json")

  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table('price-game-1')

  #allGamesForConsole_dynamoDB = table.scan(
  #  FilterExpression=Attr('console').eq(console)
  #)

  last_evaluated_key = None
  allGamesForConsole_dynamoDB = []

  # Loop through pages of scan results
  while True:
      # Perform the scan
      if last_evaluated_key:
          response = table.scan(
              FilterExpression=Attr('console').eq(console),
              ExclusiveStartKey=last_evaluated_key
          )
      else:
          response = table.scan(
              FilterExpression=Attr('console').eq(console)
          )

      # Add the results to the list
      allGamesForConsole_dynamoDB.extend(response['Items'])

      # Check if there are more items to scan
      last_evaluated_key = response.get('LastEvaluatedKey')
      
      if not last_evaluated_key:
          break  # No more items, stop the loop


  print(allGamesForConsole_dynamoDB)



  #print("dynamoDB Console stuff: ", allGamesForConsole_dynamoDB)

  #allGamesForConsole_dynamoDB
  #print(allGamesForConsole_dynamoDB["Items"][0]["title"])

  #allGamesForConsole_dynamoDB = [game["title"] for game in allGamesForConsole_dynamoDB["Items"] ]

  #print(allGamesForConsole)

  '''
  allGamesForConsole = ""
  for game in allGamesForConsole_dynamoDB["Items"]:

    allGamesForConsole += game["title"] + "\n"
  '''

  allGamesForConsole = "\n".join(game["title"] for game in allGamesForConsole_dynamoDB)

  print(allGamesForConsole)


  #print("ALL GAMES FOR CONSOLE: ", allGamesForConsole_dynamoDB)

  #print(allGamesForConsole)
  #print("----")


# "wii-u", "nintendo-switch", "playstation-4", "playstation-5", "xbox-one"]

#maybe say to not match with not for resale versions if possible and match with special versions when applicable otherwise use the base version of the game


#NOTE: LEGEND OF ZELDA IS NOT WORKING
#its thinking its The Legend of Zelda
#maybe I should implement a fuzzy search to avoid this...

#Sometimes Super Mario Bros is given a period at the end which messes everything up. This only sometimes happens.

  completion = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": [
            {
                "type": "text",
                #"text": "Print out the single game from this text file that is most likely to be the actual game. When possible include only the game and not any versions that may contain extra items or are not for resale. Print it out exactly how it is in the text and nothing else. It MUST be printed the exact way it is in the text (no extra characters).",
                "text": "Identify and print the single game name from this text file that is most likely the main game. Exclude any versions with extra items, promotional copies, or 'not for resale' labels. Print the game name exactly as it appears in the text, without adding or altering any characters. Do not add any extra flavor text.",
            },
            {
                "type": "image_url",
                "image_url": {
                  "url": image_url
                },
            },
            {
              "type": "text",
              "text": allGamesForConsole,
            },

        ]},
    ]
  )

  #print(completion.choices[0].message.content.strip())

  gameItself = completion.choices[0].message.content.strip()

  print("))))))))))))")
  #print(allGamesForConsole_dynamoDB["Super Mario Bros|nes"])

  file_name = "all_games.txt"

  # Write the list to the file
  with open(file_name, "w") as file:
      for game in allGamesForConsole:
          file.write(game + "\n")

  print(f"All games written to {file_name}")



  print("^^^^^^^^^^^^^^^^^")

  if gameItself.lower() not in allGamesForConsole.lower().split("\n"):
    print("THE GAME: ", gameItself)
    #difflib better for basically exact matches, whereas fuzzywuzzy deals better with typos
    match = difflib.get_close_matches(gameItself, allGamesForConsole.split("\n"), n=1)
    print("Fuzzy Matches:", match)
    if match:
       gameItself = match[0]
    else:
       print("HELP FIX THID!!")
  else:
     print("IT HERE!!")



  print("-------")
  print("Console: ", console, " - Game Itself: ", gameItself)

  #result = completion.choices[0].message.content.strip().split("|")

  #result = {"Game":gameItself, "Console":console}

  print("**************************")

  print(gameItself+"|"+console)

  completeGame = (gameItself+"|"+console).lower()

#  result = table.scan(
#    FilterExpression=Attr('game_id').eq(gameItself+"|"+console)
#  )




#https://stackoverflow.com/questions/46617575/python-dynamodb-scan-operation-not-return-all-records


  # Initialize variables for pagination
  last_evaluated_key = None
  all_items = []

  # Loop through pages of scan results
  while True:
      # Perform the scan
      if last_evaluated_key:
          response = table.scan(
              #FilterExpression=Attr('game_id').eq(gameItself+"|"+console),
              FilterExpression=Attr('game_id').eq(completeGame),

              ExclusiveStartKey=last_evaluated_key
          )
      else:
          response = table.scan(
              #FilterExpression=Attr('game_id').eq(gameItself+"|"+console)
              FilterExpression=Attr('game_id').eq(completeGame)

          )

      # Add the results to the list
      all_items.extend(response['Items'])

      # Check if there are more items to scan
      last_evaluated_key = response.get('LastEvaluatedKey')
      
      if not last_evaluated_key:
          break  # No more items, stop the loop

  print("&&&&&&&&&&&&&&&&&&&&&")
  print(all_items)

  #result = table.scan()

  #with open("scan_result.txt", "w", encoding="utf-8") as file:
  #  file.write(str(result))

  #print("Result written to scan_result.txt")



  #print(result)

  #return result

  return all_items[0]

