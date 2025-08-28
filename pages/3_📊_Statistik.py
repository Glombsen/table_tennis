import streamlit as st
from helper import create_match_statistic, get_player_statistic

st.set_page_config(page_title="Statistiken", page_icon="📊")

df = create_match_statistic()


event = st.dataframe(
    df.drop("date", axis=1),
    width="stretch",
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
)

selected = event.selection.rows



if selected:
    selected_player = df.iloc[selected]["Spieler"].to_numpy()[0]
    st.bar_chart(
        df[df["Spieler"] == selected_player],
        x="date",
        y="Siege",
        x_label="Datum",
    )
    for stat in get_player_statistic(selected_player):
        st.markdown("- " + stat)

else:
    line_df = df.pivot(index="date", columns="Spieler", values="Siege").fillna(0)
    st.line_chart(line_df, x_label="Datum")