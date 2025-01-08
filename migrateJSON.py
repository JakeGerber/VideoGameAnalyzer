import json
import boto3

from boto3.dynamodb.conditions import Key, Attr


#Load the JSON data
with open('combined.json', 'r') as file:
    data = json.load(file)

#Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('price-analyzer-complete-2')

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





'''
try:
    response = table.scan()  # Retrieves all items from the table
    items = response.get("Items", [])

    # Print all items
    if items:
        for item in items:
            print(item)
    else:
        print("No items found in the table.")
except Exception as e:
    print(f"Error retrieving items from the table. Error: {str(e)}")
'''





quit()

#WIP for uploading files to the S3 bucket.

s3 = boto3.resource('s3')
bucket = s3.Bucket('price-test-real')

print(bucket)



file_path = r"C:\Users\Jake\Desktop\Price Checker\Github-Repo\VideoGameAnalyzer\test.png"
object_name = "bikething|pss1.png"
bucket_name = "price-test-real"
# Upload the file to S3
#it's not alwyays a png tho...
bucket.upload_file(file_path, object_name, ExtraArgs={'ContentType': "png"})
print(f'File uploaded successfully to {bucket_name}/{object_name}')

s3.Object(bucket_name, object_name).Acl().put(ACL='public-read')
print(f'File {object_name} is now public.')


# Get the URL of the uploaded file
file_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
print(f"File URL: {file_url}")

