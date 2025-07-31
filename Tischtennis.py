
import collections as coll
import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Tischtennis",
    page_icon="🏓",
)
with open("./spieler.json") as f:
    players = json.loads(f.read())

with open("./games.json") as f:
    matches = json.loads(f.read())

print(set(match["player_one"] for match in matches))
print(set(match["player_two"] for match in matches))

punkte = coll.defaultdict(int)
spiele = coll.defaultdict(int)
siege = coll.defaultdict(int)

for player in players:
    spiele[player] = 0

for match in matches:
    p1 = match["player_one"]
    p2 = match["player_two"]
    winner_key = match["win"]

    winner = match[winner_key]
    loser = p1 if winner == p2 else p2

    punkte[winner] += 2
    punkte[loser] += 1
    spiele[p1] += 1
    spiele[p2] += 1
    siege[winner] += 1

df = pd.DataFrame(
    {
        "Spieler": list(spiele.keys()),
        "Spiele": [spiele[p] for p in spiele],
        "Siege": [siege[p] for p in spiele],
        "Punkte": [punkte[p] for p in spiele],
    }
)

df = df.sort_values(by="Punkte", ascending=False).reset_index(drop=True)

st.dataframe(df, use_container_width=True, hide_index=True)