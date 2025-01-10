import json
import boto3

from boto3.dynamodb.conditions import Key, Attr

import os


#Load the JSON data
with open('combined.json', 'r') as file:
    data = json.load(file)


#dynamodb = boto3.resource('dynamodb')
#table = dynamodb.Table('price-game-1')

#print(table.scan())

#quit()

#WIP for uploading files to the S3 bucket.


s3 = boto3.resource('s3')
bucket = s3.Bucket('price-test-real')

#print(bucket)

for key, game in data.items():
    try:
        print("key: ", key)
        print("game: ", game["cover-link"])
        file_path = game["cover-link"]
        _, file_extension = os.path.splitext(file_path)
        object_name = file_path.split("\\")[-1] + "|" + game["game-console"]
        bucket_name = "price-test-real"


        print("----+")
        print(game["game-console"])
        print("!: ", file_extension)
        print("#: ", object_name)
        print("----=")


        bucket.upload_file(file_path, object_name, ExtraArgs={'ContentType': file_extension})
        print(f'File uploaded successfully to {bucket_name}/{object_name}')

        s3.Object(bucket_name, object_name).Acl().put(ACL='public-read')
        print(f'File {object_name} is now public.')


        # Get the URL of the uploaded file
        file_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        print(f"File URL: {file_url}")

        game["cover-link"] = file_url

        print(file_url)


    except Exception as e:
        print(e)

#print("WOW")
#quit()


#Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('price-game-1')

#plan : before putting things into database, if you want to use online storage, upload
#the images in gamecoverlink to s3 bucket and update the link

for key, game in data.items():
    print("key: ", key)
    print("game: ", game["game-console"])
    
    try:
        table.put_item(
            Item={
                "game_id": key,  #Partition key
                "console": game["game-console"],  #Sort key
                **{k: v for k, v in game.items() if k != "game-console"}  #Other Information
            }
        )
        print(f"Successfully added key: {key}, game: {game['game-console']} to the table.")


    except Exception as e:
        print(f"Error adding key: {key}, game: {game['game-console']} to the table. Error: {str(e)}")
        print("Press Enter to continue...")
        input()



print("DONE")
quit()



#file_path = r"C:\Users\Jake\Desktop\Price Checker\Github-Repo\VideoGameAnalyzer\test.png"
#object_name = "bikething|pss1.png"
#bucket_name = "price-test-real"
# Upload the file to S3
#it's not alwyays a png tho...
#bucket.upload_file(file_path, object_name, ExtraArgs={'ContentType': "png"})
#print(f'File uploaded successfully to {bucket_name}/{object_name}')

#s3.Object(bucket_name, object_name).Acl().put(ACL='public-read')
#print(f'File {object_name} is now public.')


# Get the URL of the uploaded file
#file_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
#print(f"File URL: {file_url}")

print("ok")

