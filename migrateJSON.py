import json
import boto3

from boto3.dynamodb.conditions import Key, Attr


# Load the JSON data
#with open('combined.json', 'r') as file:
with open('combined.json', 'r') as file:
    data = json.load(file)

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('price-analyzer-complete')

#print(table)

testx = table.scan(
FilterExpression=Attr('game_id').eq('Mario Party 8|wii')
)
print(testx)
quit()

#-----------------
with open('dynamodb_items.json', 'w') as file:
    # Scan the table and handle pagination
    response = table.scan()

    # Write items from the first page to the file
    for item in response['Items']:
        json.dump(item, file)
        file.write('\n')  # Write each item on a new line
    
    # If there are more items, continue scanning and writing
    while 'LastEvaluatedKey' in response:
        # Get the next set of results
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])

        # Write the items to the file
        for item in response['Items']:
            json.dump(item, file)
            file.write('\n')  # Write each item on a new line

print("Data written to 'dynamodb_items.json'")

#-----------------



#print(testx)
quit()

#Uncomment since this working

for key, game in data.items():
    print("key: ", key)
    print("game: ", game["game-console"])

        
    
    try:
        table.put_item(
            Item={
                "game_id": key,  # Partition key
                "console": game["game-console"],  # Sort key
                **{k: v for k, v in game.items() if k != "game-console"}  # Additional attributes
            }
        )
        print(f"Successfully added key: {key}, game: {game['game-console']} to the table.")


    except Exception as e:
        print(f"Error adding key: {key}, game: {game['game-console']} to the table. Error: {str(e)}")
        print("Press Enter to continue...")
        input()  # Waits until the Enter key is pressed





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






#print(table.scan())
#quit()

#----------

'''
response = table.scan(
    FilterExpression=Attr('game_id').eq('Blue Marlin|nes')
)

# Print the results
for item in response['Items']:
    print(item)
'''


quit()

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

