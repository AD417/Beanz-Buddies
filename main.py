from datetime import date
from CRUD import *
from slack.read import *

from datetime import datetime

start = datetime.now()


def get_groups():
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
            
    return result

def main():
    members, frosh, active = get_groups()
    if not members:
        print("Error getting members info.")
        return

    alumni = members.difference(frosh, active)
    frosh.intersection_update(members)
    active.intersection_update(members)

    db = Database()

    pair_gen = PairingGenerator(frosh, active, alumni, db, now=date.today())

    pairs = pair_gen.make_good_pairing()

    uuids = pair_gen.everyone
    names = get_multi_user_info(uuids)
    lookup = {}
    for uuid, name in zip(uuids, names):
        lookup[uuid] = name["real_name"]

    for p1, p2 in pairs:
        print(f"({lookup[p1]}, {lookup[p2]})")
        db.add_pair(p1, p2)

    db.close()

main()

end = datetime.now()

print(f"This took {end - start} seconds, by the way.")