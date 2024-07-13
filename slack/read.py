import requests
from dotenv import load_dotenv
import os

load_dotenv()

_SLACK_TOKEN = os.getenv("SLACK_API_KEY")
CHANNEL_ID = os.getenv("BEANZ_CHANNEL_ID") # the ID of #beanz-buddies
ACTIVE_ID = os.getenv("ACTIVE_ID") # Active User ID
FROSH_ID = os.getenv("FROSH_ID") # Freshman User ID

def members_of_channel(channel_id):
    """Get a list of people in the specified channel."""
    url = 'https://slack.com/api/conversations.members'
    params = {
        'channel': channel_id,
        'limit': 1000  # Adjust limit as necessary
    }
    headers = {
        'Authorization': f'Bearer {_SLACK_TOKEN}'
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    data = response.json()
    print(data)
    if not data['ok']:
        raise Exception(f"Error getting channel members: {data['error']}")
    
    return data['members']

def members_of_group(user_group_id):
    """Get a list of people in the specified user group (Frosh, Active)"""
    url = 'https://slack.com/api/usergroups.users.list'
    params = {
        'usergroup': user_group_id
    }
    headers = {
        'Authorization': f'Bearer {_SLACK_TOKEN}'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['ok']:
            return data['users']
        else:
            raise Exception(f"Error getting user group members: {data['error']}")
    else:
        raise Exception(f"Request failed with status code {response.status_code}")

def get_user_info(user_id):
    """Get specific user info regarding a specific person."""
    url = 'https://slack.com/api/users.info'
    params = {
        'user': user_id
    }
    headers = {
        'Authorization': f'Bearer {_SLACK_TOKEN}'
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        return None
    
    data = response.json()
    if not data['ok']:
        raise Exception(f"Error getting user info: {data['error']}")
    
    return data['user']