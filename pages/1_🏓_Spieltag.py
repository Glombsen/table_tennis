import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import pandas as pd


st.set_page_config(page_title="Spieltag")

today = datetime.now().strftime("%d.%m.%Y")
my_file = Path(f"./game_day_{today.replace('.', '_')}.json")
if my_file.is_file():
    with open(f"./game_day_{today.replace('.', '_')}.json") as f:
        presence = json.loads(f.read())
else:
    presence = []

with open("./new_game.json") as f:
    matches = json.loads(f.read())

with open("./spieler.json") as f:
    players = json.loads(f.read())

if "hide" not in st.session_state:
    st.session_state.hide = False


def show_hide():
    st.session_state.hide = not st.session_state.hide


st.button("Anwesenheit", on_click=show_hide)

if st.session_state.hide:
    presence_container = st.container()
    with presence_container:
        with st.form("presence_form"):
            NUMBER_OF_COLUMNS = 3
            columns = st.columns(spec=NUMBER_OF_COLUMNS)
            items_per_col = len(players) // NUMBER_OF_COLUMNS
            for i, col in enumerate(columns):

                items_index_start = i * items_per_col
                items_index_end = (
                    (i + 1) * items_per_col
                    if i + 1 != NUMBER_OF_COLUMNS
                    else len(players)
                )

                for player in players[items_index_start:items_index_end]:
                    active = False
                    if player in presence:
                        active = True
                    col.toggle(player, key=f"presence_{player}", value=active)
            
            save_presence = st.form_submit_button("Speichern", use_container_width=True)

            if save_presence:
                presence = []
                for key in st.session_state:
                    if key.startswith("presence_"):
                        if st.session_state[key]:
                            presence.append(key.replace("presence_", ""))
                with open(f"./game_day_{today.replace('.', '_')}.json", "w+") as f:
                    json.dump(presence, f, indent=4)
                
                st.rerun()


with st.form("new_match", clear_on_submit=True):
    
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        player_one = st.selectbox(
            "Spieler 1",
            [player for player in players if player in presence],
        )
    with col2:
        win_player_one = st.form_submit_button(
            "Sieg Spieler 1", use_container_width=True
        )

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        player_two = st.selectbox(
            "Spieler 2",
            [player for player in players if player in presence],
        )
    with col2:
        win_player_two = st.form_submit_button(
            "Sieg Spieler 2", use_container_width=True
        )
    
    if win_player_one:
        matches.append(
            {
                "date": today,
                "winner": player_one,
                "looser": player_two,
            }
        )
        with open("./new_game.json", "w+") as f:
            json.dump(matches, f, indent=4)
        st.rerun()
    if win_player_two:
        matches.append(
            {
                "date": today,
                "winner": player_two,
                "looser": player_one,
            }
        )
        with open("./new_game.json", "w+") as f:
            json.dump(matches, f, indent=4)
        st.rerun()

match_day = []
for match in matches:
    if match["date"] == today:
        match_day.append(
            {
                "Sieg": match["winner"],
                "Verloren": match["looser"],
            }
        )

df = pd.DataFrame.from_dict(match_day)
st.dataframe(df, use_container_width=True, hide_index=True)