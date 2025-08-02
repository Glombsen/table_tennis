import streamlit as st
import json
import altair as alt
from helper import create_match_statistic

st.set_page_config(page_title="Statistiken", page_icon="📊")

player = None
if "Spieler" in st.query_params:
    player = st.query_params["Spieler"]

df = create_match_statistic(player)

st.dataframe(df, use_container_width=True, hide_index=True)

if "Spieler" in st.query_params:
    st.bar_chart(df, x="Datum", y="Siege")
else:
    df = df.pivot(index="Datum", columns="Spieler", values="Siege").fillna(0)
    st.line_chart(df)