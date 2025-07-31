import streamlit as st
import json
from datetime import datetime
import pandas as pd


st.set_page_config(page_title="Spieltag")

with open("./games.json") as f:
    matches = json.loads(f.read())

with open("./spieler.json") as f:
    players = json.loads(f.read())

with st.form("new_match", clear_on_submit=True):
    
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        player_one = st.selectbox(
            "Spieler 1",
            players,
        )
    with col2:
        win_player_one = st.form_submit_button(
            "Sieg Spieler 1", use_container_width=True
        )

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        player_two = st.selectbox(
            "Spieler 2",
            players,
        )
    with col2:
        win_player_two = st.form_submit_button(
            "Sieg Spieler 2", use_container_width=True
        )
    
    if win_player_one:
        matches.append(
            {
                "date": datetime.now().strftime("%d.%m.%Y"),
                "player_one": player_one,
                "player_two": player_two,
                "win": "player_one",
            }
        )
        with open("./games.json", "w+") as f:
            json.dump(matches, f, indent=4)
        st.rerun()
    if win_player_two:
        matches.append(
            {
                "date": datetime.now().strftime("%d.%m.%Y"),
                "player_one": player_one,
                "player_two": player_two,
                "win": "player_two",
            }
        )
        with open("./games.json", "w+") as f:
            json.dump(matches, f, indent=4)
        st.rerun()

match_day = []
for match in matches:
    if match["date"] == datetime.now().strftime("%d.%m.%Y"):
        match_day.append(
            {
                "Spieler 1": match["player_one"],
                "Spieler 2": match["player_two"],
                "Sieg": match[match["win"]],
            }
        )

df = pd.DataFrame.from_dict(match_day)
st.dataframe(df, use_container_width=True, hide_index=True)