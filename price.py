import boto3
import textract_wrapper

import difflib

import os

import chardet

import numpy as np

import cv2

from fuzzywuzzy import process

#I am using Amazon CLI for credentials.



def listOfAllGames(txtFilePath, matches = []):
    #txtFilePath = r"C:\Users\Jake\Desktop\Price Checker\PS1-GamesList.txt"

    with open(txtFilePath, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print(f"Detected encoding: {encoding}")





    # Open the file
    with open(txtFilePath, 'r', encoding=encoding) as file:
        # Iterate over each line in the file
        for line in file:
            # Strip any leading/trailing whitespace characters (e.g., newline)
            line = line.strip()
            # Print the line or perform other processing
            print(line)
            if (len(line) > 0):
                matches.append(line[1:-1])

    return matches


#This needs to be updated so the key for images uploaded is different.
#NOT CORRECT
def uploadImageToS3Bucket(filePath, fileKey, bucketName):
    #This code makes it so it uploads image to S3 bucket, changes contentType so it is inline instead of download
    #and it changes ACL access to public read.
    try:
        with open(filePath, 'rb') as data:
            # Upload the image to S3 with the correct content type
            s3.Bucket(bucketName).put_object(
                Bucket=bucketName,
                Key=fileKey,
                Body=data,
                ContentType="image/jpg",
                ACL='public-read'
            )
        print("File uploaded successfully.")
    except Exception as e:
        print("ERROR: ", e)



# This is my test price

s3 = boto3.resource('s3')
textractmodule = boto3.client("textract")
dynamodbmodule = boto3.client("dynamodb")



response = dynamodbmodule.list_tables() #dynamodbmodule.describe_table(TableName="TestTable")

print(response)


# Function to add an item to the DynamoDB table using the client
def add_entry_to_dynamodb(id: str, name: str, platform: str):
    response = dynamodbmodule.put_item(
        TableName='PriceTableTest',  # Table name here
        Item={
            'game_id': {'S': id},          # 'S' denotes that the type of the attribute is a string
            'name': {'S': name},
            'platform': {'S': platform}
        }
    )
    return response

# Example usage
response = add_entry_to_dynamodb('ds', 'dfgsdf', 'POI')

print(response)


def scan_table():
    response = dynamodbmodule.scan(
        TableName='PriceTableTest'  # Table name here
    )
    return response

# Retrieve all items
response = scan_table()

# Print all items in the table
items = response.get('Items', [])
for item in items:
    print(item)



quit()





for bucket in s3.buckets.all():
    print(bucket.name)


ps1_file_path = r"C:\Users\Jake\Desktop\Price Checker\PS1-GamesList.txt"

matches = listOfAllGames(txtFilePath=ps1_file_path)



#uploadImageToS3Bucket()

#Maybe have user option where they could either see price or add to their collection.


#response = dynamodbmodule.list_tables()

#print(response)

#quit()



logo = cv2.imread(r"C:\Users\Jake\Desktop\Price Checker\Wii-Logo2.jpg")

logoList = []

for filename in os.listdir("Logos"):
    #print(filename)
    logoList.append(filename)
    #logoList.append(cv2.imread("Logos\\" + filename))


#image = cv2.imread(r"C:\Users\Jake\Desktop\Price Checker\super.jpg")

#imageList = []

#Test
# Load the main image and the logo
image = cv2.imread(r"C:\Users\Jake\Desktop\Price Checker\mario.jpg")
logoRead = cv2.imread(r"C:\Users\Jake\Desktop\Price Checker\Logos\Wii-Logo-White.jpg")

# Check if images are loaded
if image is None:
    print("Error loading main image")
if logoRead is None:
    print("Error loading logo image")

# Convert images to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_logo = cv2.cvtColor(logoRead, cv2.COLOR_BGR2GRAY)

# Perform template matching
result = cv2.matchTemplate(gray_image, gray_logo, cv2.TM_CCOEFF_NORMED)

# Set the threshold
threshold = 0.8
loc = np.where(result >= threshold)

# Check if any matches are found
if len(loc[0]) > 0:
    print("!!!FOUND Logo found in the image.")
    # Draw rectangles around matched regions
    w, h = gray_logo.shape[::-1]
    for pt in zip(*loc[::-1]):
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
    # Save or display the result image
    cv2.imwrite(r"C:\Users\Jake\Desktop\Price Checker\result.jpg", image)
else:
    print("Not found..")

#Test-End


if len(loc[0]) > 0:
    print("!!!FOUND Logo found in the image.")


quit()

for filename in os.listdir("Recognizing-Games"):

    #image = cv2.imread("Recognizing-Games\\" + filename)

    image = cv2.imread(r"C:\Users\Jake\Desktop\Price Checker\mario.jpg")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for logo in logoList:
        print(logo)

        #logoRead = cv2.imread("Logos\\" + logo)

        logoRead = cv2.imread(r"C:\Users\Jake\Desktop\Price Checker\Logos\Wii-Logo-White.jpg")
        gray_logo = cv2.cvtColor(logoRead, cv2.COLOR_BGR2GRAY)
        

        result = cv2.matchTemplate(gray_image, gray_logo, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8
        loc = np.where(result >= threshold)

        cv2.imshow('Detected Logos', image)

        #cv2.imwrite('result.png', image)
        cv2.waitKey(0)



        if len(loc[0]) > 0:
            print("!!!FOUND Logo found in the image.")
        #else:
        #    print("Logo not found in the image.")

        

        #print("RESULT: ", loc)

        #for pt in zip(*loc[::-1]):
        #    cv2.rectangle(image, pt, (pt[0] + logo.shape[1], pt[1] + logo.shape[0]), (0, 255, 0), 2)




    #print(filename)
    #imageList.append(filename)


'''

gray_logo = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


result = cv2.matchTemplate(gray_image, gray_logo, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(result >= threshold)

print("GOT HERE!")

for pt in zip(*loc[::-1]):
    cv2.rectangle(image, pt, (pt[0] + logo.shape[1], pt[1] + logo.shape[0]), (0, 255, 0), 2)

# Save or display the result
cv2.imwrite('result.png', image)
cv2.imshow('Detected Logos', image)
cv2.waitKey(0)

'''

#quit()


'''
response = textractmodule.detect_document_text(
    Document={
        "S3Object" : {
            "Bucket": "price-checker-images",
            "Name": "super.jpg"
        }
    }
)

print ('------------- Print Plaintext detected text ------------------------------')
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print ('\033[92m'+item["Text"]+'\033[92m')
'''

playstationNotDetected = []

directory_path = "PS1-Tests"

for filename in os.listdir(directory_path):
    print(filename)

    extension = filename.split(".")[-1]

    print(extension)

    contentType = "image/" + extension

    
    with open(directory_path + "/" + filename, 'rb') as data:
        # Upload the image to S3 with the correct content type
        s3.Bucket('price-checker-images').put_object(
            Bucket='price-checker-images',
            Key=filename,
            Body=data,
            ContentType=contentType,
            ACL='public-read'
        )


    response = textractmodule.detect_document_text(
    Document={
        "S3Object" : {
            "Bucket": "price-checker-images",
            "Name": filename
                }
            }
        )


    containsType = False

    #Note: Sometimes it cant differentiate between PS1 and PS2 because it thinks the copyright is a period

    finalTest = ""

    #matches = ["Super Smash Bros", "Nintendo Land", "Kirby and the Mirror", "Simpsons Hit and Run", "Zelda Tears of the Kingdom"]

    #They should always be on the same line.
    print ('------------- Print Plaintext detected text ------------------------------')
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print ('\033[92m'+item["Text"]+'\033[92m')
            if ("playstation" in item["Text"].lower() and "2" in item["Text"].lower()):
                print("WOW A PS2")
            elif ("playstation" in item["Text"].lower()):
                print("YAY")
            elif ("wii" in item["Text"].lower()):
                print("WIIIIIIII")
            else:
                finalTest += (item["Text"] + " ")
    
    print("*************************")

    print(finalTest)

    #difflib.get_close_matches(finalTest, matches)

    print("----------------------")

    matched = process.extract(finalTest, matches, limit=10)

    for m in matched:
        print(f"Match: {m[0]}, Score: {m[1]}")

    print("closest match!")
    print("*************************")

