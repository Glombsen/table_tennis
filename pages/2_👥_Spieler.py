import streamlit as st
import json

st.set_page_config(page_title="Spieler")

with open("./spieler.json") as f:
    players = json.loads(f.read())


with st.form("new_player", clear_on_submit=True):
    player = st.text_input("Neuer Spieler", key="new_player_input")
    submitted = st.form_submit_button("Submit")
    if submitted:
        players.append(player)
        with open("./spieler.json", "w+") as f:
            json.dump(players, f, indent=4)
        st.rerun()

st.table(players)