from datetime import date
from slack.read import *

from datetime import datetime

start = datetime.now()

def main():
    members = set(members_of_channel(CHANNEL_ID))
    frosh = set(members_of_group(FROSH_ID))
    active = set(members_of_group(ACTIVE_ID))
    if not members:
        print("Error getting members info.")
        return
    
    alumni = members.difference(frosh, active)
    frosh.intersection_update(members)
    active.intersection_update(members)
    
    print("Freshmen:")
    for member in frosh:
        user_info = get_user_info(member)
        if not user_info:
            print(f"Failed to get info for member {member}.")
            continue

        print(user_info["real_name"])

    print("\nUpperclassmen:")
    for member in active:
        user_info = get_user_info(member)
        if not user_info:
            print(f"Failed to get info for member {member}.")
            continue

        print(user_info["real_name"])

    print("\nAlumni:")
    for member in alumni:
        user_info = get_user_info(member)
        if not user_info:
            print(f"Failed to get info for member {member}.")
            continue

        print(user_info["real_name"])

main()

end = datetime.now()

print(f"This took {end - start} seconds, by the way.")