from CRUD import *
from datetime import date
from slack.read import *
from concurrent.futures import ThreadPoolExecutor, as_completed

from datetime import datetime

start = datetime.now()

def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        api_calls = {
            executor.submit(members_of_channel, CHANNEL_ID): 0,
            executor.submit(members_of_group, FROSH_ID): 1,
            executor.submit(members_of_group, ACTIVE_ID): 2
        }
        result = [None] * len(api_calls)

        for future in as_completed(api_calls):
            index = api_calls[future]
            try:
                member_data = future.result()
                result[index] = set(member_data)
            except Exception as e:
                raise Exception("API issue getting member info: ") from e
            
    

    members, frosh, active = result
    if not members:
        print("Error getting members info.")
        return
    
    alumni = members.difference(frosh, active)
    frosh.intersection_update(members)
    active.intersection_update(members)
    
    print("Freshmen:")
    for member in get_multi_user_info(list(frosh)):
        if not member:
            print(f"Failed to get info for member.")
            continue

        print(member["real_name"])

    print("\nUpperclassmen:")
    for member in get_multi_user_info(list(active)):
        if not member:
            print(f"Failed to get info for member.")
            continue

        print(member["real_name"])

    print("\nAlumni:")
    for member in get_multi_user_info(list(alumni)):
        if not member:
            print(f"Failed to get info for member.")
            continue

        print(member["real_name"])

main()

end = datetime.now()

print(f"This took {end - start} seconds, by the way.")