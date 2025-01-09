from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import connectionAI
import fuzzysearch
import json

import streetAPI

import boto3

from boto3.dynamodb.conditions import Key, Attr



def retrieveJSON_data(game, JSON_file):

    with open(JSON_file, 'r') as file:
        data = json.load(file)

    print("Game is: ", game)
    #print(data)

    #print(f"Zelda: Tears Of the Kingdom|nintendo-switch" == game.strip())

    loadedGame = data.get(game, None)
    if (loadedGame == None):
        print("ERROR loading game")

    print("THIS IS LOADED: ", loadedGame)
    print("f: ", JSON_file)

    base_image_path = os.getenv('BASE_IMAGE_PATH')
    #"C:\Users\Jake\Desktop\Price Checker\Github-Repo\VideoGameAnalyzer\.env"

    print("Base Image Path: ", base_image_path)


    loadedGame["cover-link"] = base_image_path + "\\" + loadedGame["cover-link"]

    print("New link is: ", loadedGame["cover-link"])

    return {game : loadedGame}

#for dynamodb
#def retrive_data(game):

#maybe add all table names to env file?
def retrieve_dynamodb_data(game):
    print(game)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('price-game-1')


    last_evaluated_key = None
    gameFound = []

    #THIS CODE NEEDS TO BE REFACTORED

    # Loop through pages of scan results
    while True:
        # Perform the scan
        if last_evaluated_key:
            response = table.scan(
                FilterExpression=Attr('game_id').eq(game),
                ExclusiveStartKey=last_evaluated_key
            )
        else:
            response = table.scan(
                FilterExpression=Attr('game_id').eq(game)
            )

        # Add the results to the list
        gameFound.extend(response['Items'])

        # Check if there are more items to scan
        last_evaluated_key = response.get('LastEvaluatedKey')
        
        if not last_evaluated_key:
            break  # No more items, stop the loop

    print("FOUND IT!: ")
    print(gameFound)
    loadedGame = gameFound[0]

    return {game : loadedGame}




app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

useLocalJSON = False

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    ai_information = connectionAI.connectToAI(file_path)

    if ai_information["title"] == "unknown" or ai_information["console"] == "unknown":
        print("ERROR! NOT VALID IMAGE!")
        #probably return error messasge here
    
    print("ai_information_is: ",  ai_information)

    ai_information["game_id"] = ai_information["game_id"].lower()

    return jsonify({ai_information["game_id"] : ai_information}), 200

    #return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200



@app.route('/upload_text', methods=['POST'])
def upload_text():
    try:
        # Retrieve text from the request body (JSON format)
        if request.is_json:
            data = request.get_json()
            text = data.get('text', '')
            console = data.get('console', '')
        else:
            # Alternatively, retrieve text from form data
            text = request.form.get('text', '')
            console = request.form.get('console', '')

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Process or save the text as needed
        # For demonstration, we'll just return it
        #return jsonify({"message": "Text uploaded successfully", "text": text}), 200

        fuzzySearchResponse = fuzzysearch.search(game=text, console=console, topN=5)

        print("This is the fuzzy response wow!: ", fuzzySearchResponse)

        return jsonify({"message": "Text uploaded successfully", "text": fuzzySearchResponse}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



#Need to migrate off the JSON files
@app.route('/upload_title', methods=['POST'])
def upload_title():
    print("UPLOADING TITLE!")
    try:
        # Retrieve text from the request body (JSON format)
        if request.is_json:
            data = request.get_json()
            print("DATA!: ", data)
            text = data.get('text', '')
        else:
            # Alternatively, retrieve text from form data
            text = request.form.get('text', '')

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Process or save the text as needed
        # For demonstration, we'll just return it
        #return jsonify({"message": "Text uploaded successfully", "text": text}), 200

        print("title text is: ", text)

        #print(retrieveJSON_data(text, f"./Game-JSONs/{text.split("|")[-1]}_Information.json"))

        #The issue with using the local JSON is path stuff.
        if useLocalJSON:
            return jsonify(retrieveJSON_data(text, f"./Game-JSONs/{text.split("|")[-1]}_Information.json")), 200
        else:
            print("Need to add database support here")
            return jsonify(retrieve_dynamodb_data(text)), 200
            

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/upload_address', methods=['POST'])
def upload_address():
    print("UPLOADING ADDRESS!")
    try:
        # Retrieve text from the request body (JSON format)
        if request.is_json:
            data = request.get_json()
            print("DATA!: ", data)
            text = data.get('text', '')
        else:
            # Alternatively, retrieve text from form data
            text = request.form.get('text', '')

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Process or save the text as needed
        # For demonstration, we'll just return it
        #return jsonify({"message": "Text uploaded successfully", "text": text}), 200

        print("title text is: ", text)

        #print(retrieveJSON_data(text, f"./Game-JSONs/{text.split("|")[-1]}_Information.json"))

        return jsonify(streetAPI.search_location(text)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
