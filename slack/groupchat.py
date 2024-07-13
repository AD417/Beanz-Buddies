import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

_SLACK_TOKEN = os.getenv("SLACK_API_KEY")
MIRAI_UUID = os.getenv("MIRAI_UUID")  # Replace with your user ID

def create_group_chat(user_ids):
    """
    Attempts to create a group chat containing the provided inviduals.
    Returns the ID of the channel. If the chat already exists, returns its id.
    """
    url = 'https://slack.com/api/conversations.open'
    headers = {
        'Authorization': f'Bearer {_SLACK_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'users': ','.join(user_ids)
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    
    data = response.json()
    if not data['ok']:
        raise Exception(f"Error creating group chat: {data['error']}")
    
    return data['channel']['id']

def send_welcome_message(channel_id, message):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f'Bearer {_SLACK_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'channel': channel_id,
        'text': message
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    
    data = response.json()
    if not data['ok']:
        raise Exception(f"Error sending message: {data['error']}")
    
    print("Message sent successfully: '" + message + "'")

def main():
    user_ids = [MIRAI_UUID, input("Another user's ID: ")]
    channel_id = create_group_chat(user_ids)
    if channel_id:
        print(channel_id)
        welcome_message = f"God dammit Mirai stop testing this"
        send_welcome_message(channel_id, welcome_message)

if __name__ == '__main__':
    main()