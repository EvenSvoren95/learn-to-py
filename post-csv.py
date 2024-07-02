import os
import json
import requests
import csv
from dotenv import load_dotenv
from shutil import move
from datetime import datetime

# Load environment variables
load_dotenv()

# API
API_URL = os.getenv('API_URL')
ENDPOINT_POST_TEMPLATE = os.getenv('ENDPOINT_POST_TEMPLATE')

# Credentials for API
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Define store
STORE = os.getenv('STORE')
COMPANY = os.getenv('COMPANY')

# Log file directory
LOG_DIR = "logs"
TODAY_DATE = datetime.now().strftime("%d%m%Y")
LOG_FILE = os.path.join(LOG_DIR, f"log_{TODAY_DATE}.txt")

# Ensure the log folder exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

#Writes a logfile for API error
def log_response(message):
    with open(LOG_FILE, "a", encoding='latin1') as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

#Generates the token 
def generate_token():
    url = f"{API_URL}/token"
    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    response = requests.post(url, json=payload)
    print(f"Response status code: {response.status_code}")
    print(f"Response text (token generation): {response.text}")
    log_response(f"Token generation response status code: {response.status_code}, response text: {response.text}")
    if response.status_code == 200:
        try:
            data = response.json()
            access_token = data.get("responseMessage", {}).get("access_token")
            refresh_token = data.get("responseMessage", {}).get("refresh_token")
            return access_token, refresh_token
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            log_response(f"JSON decode error: {e}")
            return None, None
        except KeyError as e:
            print(f"Key error: {e}")
            log_response(f"Key error: {e}")
            return None, None
    else:
        print(f"Failed to generate token: {response.status_code}")
        print(f"Error details: {response.text}")
        log_response(f"Failed to generate token: {response.status_code}, Error details: {response.text}")
        return None, None

#Processes and sends the csv file 
def process_csv_and_send(api_token, csv_file):
    processed_folder = "Processed"
    articles = []  # Initialize an empty list to hold the articles
    all_responses_successful = True  # Initialize the success flag

    # Attempt to open the CSV file with different encodings
    try:
        with open(csv_file, mode='r', newline='', encoding='latin1') as file:
            reader = csv.reader(file, delimiter='|')  # Specify the delimiter
            for product in reader:
                if len(product) < 7 or product[0] == "EMPTY":  # Ensure the row has at least 7 elements and articleID/itemID is not empty
                    print(f"Invalid row: {product}")
                    log_response(f"Invalid row: {product}")
                    continue

                # Create an article dictionary
                article = {
                    "store": STORE,
                    "articleId": product[0],
                    "articleName": product[1],
                    "data": {
                        "STORE_CODE": STORE,
                        "ITEM_ID": product[0],
                        "ITEM_NAME": product[1],
                        "ITEM_DESCRIPTION": product[2],
                        "BARCODE": product[3],
                        "INVENTORY": product[4],
                        "LIST_PRICE": product[5],
                        "SALE_PRICE": product[6],
                        "NFC_DATA": ""
                    }
                }
                articles.append(article)  # Add the article to the list
    except UnicodeDecodeError as e:
        log_response(f"UnicodeDecodeError: {e}. Attempting to read with 'utf-8' encoding.")
        try:
            with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='|')  # Specify the delimiter
                for product in reader:
                    if len(product) < 7 or product[0] == "EMPTY":  # Ensure the row has at least 7 elements and articleID/itemID is not empty
                        print(f"Invalid row: {product}")
                        log_response(f"Invalid row: {product}")
                        continue

                    # Create an article dictionary
                    article = {
                        "store": STORE,
                        "articleId": product[0],
                        "articleName": product[1],
                        "nfcUrl": "www.sensornordic.no",
                        "data": {
                            "STORE_CODE": STORE,
                            "ARTICLEID": product[0],
                            "ITEM_NAME": product[1],
                            "ITEM_DESCRIPTION": product[2],
                            "BARCODE": product[3],
                            "INVENTORY": product[4],
                            "LIST_PRICE": product[5],
                            "SALE_PRICE": product[6]
                        }
                    }
                    articles.append(article)  # Add the article to the list
        except UnicodeDecodeError as e:
            log_response(f"Failed to read file with 'utf-8' encoding as well. UnicodeDecodeError: {e}")
            return  # Exit the function if the file cannot be read
       
    # Format the endpoint URL with the company and store
    endpoint_post = ENDPOINT_POST_TEMPLATE.format(company=COMPANY, store=STORE)

    # Send payload to API
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{API_URL}/{endpoint_post}", headers=headers, data=json.dumps(articles))
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    log_response(f"API response status code: {response.status_code}, response text: {response.text}")

    # Check if the response was successful
    if response.status_code != 200:
        all_responses_successful = False

    # Move the file if all responses were successful
    if all_responses_successful:
        # Rename and move the processed file to the "Processed" folder
        if not os.path.exists(processed_folder):
            os.makedirs(processed_folder)

        # Get the current date and time
        current_time = datetime.now().strftime("%d%m%Y%H%M")
        # Construct the new file name
        base_name = os.path.basename(csv_file)
        new_file_name = f"{current_time}-{base_name}"
        new_file_path = os.path.join(processed_folder, new_file_name)
        
        move(csv_file, new_file_path)
        print(f"Moved and renamed file to: {new_file_path}")
        log_response(f"Moved and renamed file to: {new_file_path}")
    else:
        print("File not processed due to unsuccessful API response.")
        log_response("File not processed due to unsuccessful API response.")
def main():
    # Generate API token
    access_token, _ = generate_token()
    if access_token:
        new_folder = "New"
        for file_name in os.listdir(new_folder):
            if file_name.endswith(".csv"):
                csv_file = os.path.join(new_folder, file_name)
                print(f"Processing file: {csv_file}")
                log_response(f"Processing file: {csv_file}")
        process_csv_and_send(access_token, csv_file)
    else:
        print("Token generation failed. Exiting...")
        log_response("Token generation failed. Exiting...")

if __name__ == "__main__":
    main()