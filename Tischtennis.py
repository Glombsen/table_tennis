
import collections as coll
import streamlit as st
import pandas as pd
import json

from helper import create_match_statistic

# Initialize connection.
#conn = st.connection("mysql", type="sql")

# Perform query.
#df = conn.query("SELECT * from mytable;", ttl=600)

# Print results.
#for row in df.itertuples():
#    st.write(f"{row.name} has a :{row.pet}:")

st.set_page_config(
    page_title="Tischtennis",
    page_icon="🏓",
)
with open("./spieler.json") as f:
    players = json.loads(f.read())

with open("./new_game.json") as f:
    matches = json.loads(f.read())


punkte = coll.defaultdict(int)
spiele = coll.defaultdict(int)
siege = coll.defaultdict(int)

for player in players:
    spiele[player] = 0

for match in matches:
    p1 = match["winner"]
    p2 = match["looser"]

    punkte[match["winner"]] += 2
    punkte[match["looser"]] += 1
    spiele[p1] += 1
    spiele[p2] += 1
    siege[match["winner"]] += 1

history = create_match_statistic(pivot=True)

df = pd.DataFrame(
    {
        "Spieler": list(spiele.keys()),
        "Spiele": [spiele[p] for p in spiele],
        "Siege": [siege[p] for p in spiele],
        "Punkte": [punkte[p] for p in spiele],
        "Historie": [history[player].to_list() for player in list(spiele.keys())],
    }
)

df = df.sort_values(by="Punkte", ascending=False).reset_index(drop=True)

st.dataframe(
    df,
    column_config={
        "Historie": st.column_config.LineChartColumn(
            y_min=0, y_max=30
        )
    },
    width='stretch',
    hide_index=True,
)