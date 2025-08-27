import json

with open("games.json") as file:
    game_list = json.load(file)

new_game_list = []
for game in game_list:
    if game["win"] == "player_one":
        winner = game["player_one"]
        looser = game["player_two"]
    else:
        winner = game["player_two"]
        looser = game["player_one"]
    new_game_list.append(
        {
            "date": game["date"],
            "winner": winner,
            "looser": looser,
        }
    )
with open("new_game.json", "w+") as file:
    file.write(json.dumps(new_game_list, indent=4))