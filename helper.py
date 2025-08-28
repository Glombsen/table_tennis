import collections as coll
import json
from pathlib import Path
import pandas as pd
import numpy as np

def create_match_statistic(pivot=False):
    match_days = coll.defaultdict(list)

    for file in Path("./").iterdir():
        if file.is_file() and file.name.startswith("match"):
            with open(file.resolve()) as f:
                match_date = file.stem.split("_")[1]
                match_days[match_date] = json.loads(f.read())

    with open("./new_game.json") as f:
        matches = json.loads(f.read())

    df = pd.DataFrame().from_dict(matches)


    def get_winner(row):
        return row["winner"]
    
    #def get_looser(row):
    #    if row["win"] == "player_one":
    #        return row["player_two"]
    #    return row["player_one"]

    #df["Spieler1"] = df.apply(get_winner, axis=1)
    #df["Spieler2"] = df.apply(get_looser, axis=1)

    #df["Punkte"] = (
    #    df.groupby(by=["date", "Spieler1"]).size().reset_index(name="Punkte")["Punkte"]
    #)
    #df["Punkte"] = df["Punkte"] * 2
    #df["Finale"] = (
    #    df.groupby(by=["date", "Spieler2"]).size().reset_index(name="Finale")["Finale"]
    #)
    #df = df.rename(columns={"date": "Datum", "Spieler1": "Spieler"})
    #df = df.sort_values(by=["Datum", "Punkte"], ascending=False).reset_index(drop=True)


    df["Spieler"] = df.apply(get_winner, axis=1)

    df = df.groupby(by=["date", "Spieler"]).size().reset_index(name="Siege")
    df = df.rename(columns={"date": "Datum"})
    df["date"] = pd.to_datetime(df["Datum"], dayfirst=True)
    df = df.sort_values(by=["date", "Siege"], ascending=False).reset_index(drop=True)
    
    if pivot:
        with open("./spieler.json") as f:
            players = json.loads(f.read())
        df = df.pivot(index="date", columns="Spieler", values="Siege")
        
        for pl in players:
            if pl not in df:
                df[pl] = np.nan
                
        return df.fillna(0)
    return df

def get_player_statistic(player):
    stats = []
    with open("./new_game.json") as f:
        matches = json.loads(f.read())

    df = pd.DataFrame().from_dict(matches)

    opponent_df = df.groupby(["winner", "looser"]).size().reset_index(name="w_counts")

    most_win_df = df.groupby(["winner", "date"]).size().reset_index(name="w_counts")
    most_points_df = df.groupby(["looser", "date"]).size().reset_index(name="l_counts")
    most_points_df = pd.merge(
        left=most_win_df,
        right=most_points_df,
        how="left",
        left_on=["winner", "date"],
        right_on=["looser", "date"],
    )
    most_points_df["points"] = most_points_df["w_counts"] + most_points_df["l_counts"]
    most_points_df = most_points_df.fillna(0)
    
    most_points_df = most_points_df[(most_points_df["winner"] == player)]
    most_points = most_points_df[
        (most_points_df["points"] == most_points_df["points"].max())
    ].to_dict(orient="records")
    most_win_df = most_win_df[(most_win_df["winner"] == player)]
    most_win = most_win_df[(most_win_df["w_counts"] == most_win_df["w_counts"].max())
    ].to_dict(orient="records")

    winner_df = opponent_df[(opponent_df["winner"] == player)]
    winner = winner_df[
        (winner_df["w_counts"] == winner_df["w_counts"].max())
    ].to_dict(orient="records")

    looser_df = opponent_df[(opponent_df["looser"] == player)]
    looser = looser_df[(looser_df["w_counts"] == looser_df["w_counts"].max())].to_dict(
        orient="records"
    )
    
    stats.append(
        f"Punkreichster Tag am {most_points[0]['date']} ({most_points[0]['points']})"
    )
    stats.append(
        f"Siegreichster Tag am {most_win[0]['date']} ({most_win[0]['w_counts']})"
    )
    stats.append(f"Am meisten gegen {winner[0]['looser']} gewonnen")
    stats.append(f"Am meisten gegen {looser[0]['winner']} verloren")
    return stats