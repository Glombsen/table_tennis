import streamlit as st
from helper import create_match_statistic, get_player_statistic

st.set_page_config(page_title="Statistiken", page_icon="📊")

df = create_match_statistic()

#def on_selection():
#    if not event["selection"]["rows"]:
#        if "selected_player" in st.session_state:
#            del st.session_state["selected_player"]
#    else:
#        selected_series = df.iloc[event["selection"]["rows"][0] - 1]
#        st.session_state.selected_player = selected_series["Spieler"]

event = st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
)

selected = event.selection.rows



if "Spieler" in st.query_params:
    st.bar_chart(df, x="Datum", y="Siege")
else:
    line_df = df.pivot(index="Datum", columns="Spieler", values="Siege").fillna(0)
    st.line_chart(line_df)

if selected:
    selected_player = df.iloc[selected]["Spieler"].to_numpy()[0]
    for stat in get_player_statistic(selected_player):
        st.markdown("- " + stat)