from dotenv import load_dotenv
import os
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build
load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Don't play in this
input_prompt = """
            Welcome! You've been assigned the task of assisting in accurately identifying files titles. Below, you'll find a list of files titles, each with its own unique identifier. When prompted with a query asking for a book title, please ensure to provide the correct title based on the options provided.

            Please note the following guidelines:
            1. Read each query carefully to understand the specific file title being requested.
            2. Ensure to respond with the exact title as listed in the provided options.
            3. Some file titles are the same with little changes, so include all in the result.
            
            Your task is to provide the correct title from this list in response to each query. Please ensure accuracy in your responses

            Here is the list of book titles:"""
            
def get_gemini_response(input,files,prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input,files,prompt])
    return response.text

# Add the main folder ID here you can find it in the url of the folder
folder_id = '1a95tOgSyj3RiQ1YZsaK95WTFdB1JdeRE'

def update_google_drive_content():
    scope = ['https://www.googleapis.com/auth/drive']
    # add your json key name here
    service_account_json_key = 'hti-20211079-69427080a883.json'
    credentials = service_account.Credentials.from_service_account_file(
                                filename=service_account_json_key, 
                                scopes=scope)
    service = build('drive', 'v3', credentials=credentials)
    results = service.files().list(pageSize=1000, fields="nextPageToken, files(id, name)", q = f"mimeType = 'application/vnd.google-apps.folder' and parents = '{folder_id}'").execute()
    items = results.get('files')
    files_list = []
    [files_list.append(item['name']+'\n') for item in items]
    with open('file_names.txt', 'w', encoding="utf-8") as file:
        file.writelines(files_list)
    return items
