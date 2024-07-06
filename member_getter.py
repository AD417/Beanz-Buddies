import requests
from dotenv import load_dotenv
import os

load_dotenv()
SLACK_TOKEN = os.getenv("SLACK_API_KEY")
CHANNEL_ID = os.getenv("BEANZ_CHANNEL_ID")

def get_channel_members(channel_id):
    url = 'https://slack.com/api/conversations.members'
    params = {
        'channel': channel_id,
        'limit': 1000  # Adjust limit as necessary
    }
    headers = {
        'Authorization': f'Bearer {SLACK_TOKEN}'
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        return None
    data = response.json()
    print(data)
    if not data['ok']:
        print(f"Error getting channel members: {data['error']}")
        return None
    
    return data['members']

def get_user_info(user_id):
    url = 'https://slack.com/api/users.info'
    params = {
        'user': user_id
    }
    headers = {
        'Authorization': f'Bearer {SLACK_TOKEN}'
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        return None
    
    data = response.json()
    if not data['ok']:
        print(f"Error getting user info: {data['error']}")
        return None
    
    return data['user']

def main():
    members = get_channel_members(CHANNEL_ID)
    if not members:
        print("Error getting members info.")
        return
    
    for member in members:
        user_info = get_user_info(member)
        if not user_info:
            print(f"Failed to get info for member {member}.")
            continue

        print(user_info["real_name"])

if __name__ == '__main__':
    main()