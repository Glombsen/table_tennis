import json

with open("26022025.txt") as file:
    lines = [line.rstrip() for line in file if line.rstrip() != ""]

json_list = []

for idx, line in enumerate(lines):
    print(idx)
    splitted = line.split()
    date = "26.08.2025"
    player_one = splitted[0]
    player_two = splitted[4]

    if splitted[1] == "1":
        win = "player_one"
    else:
        win = "player_two"

    json_list.append({"date": date, "player_one": player_one, "player_two": player_two, "win": win})
print(json_list)