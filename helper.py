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

    with open("./games.json") as f:
        matches = json.loads(f.read())

    df = pd.DataFrame().from_dict(matches)


    def get_winner(row):
        return row[row["win"]]
    
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
    df = df.sort_values(by=["Datum", "Siege"], ascending=False).reset_index(drop=True)
    
    if pivot:
        with open("./spieler.json") as f:
            players = json.loads(f.read())
        df = df.pivot(index="Datum", columns="Spieler", values="Siege")
        
        for pl in players:
            if pl not in df:
                df[pl] = np.nan
                
        return df.fillna(0)
    return df

def get_player_statistic(player):
    stats = []
    df = create_match_statistic()
    df = df.loc[df["Spieler"] == player]
    most_win = df[df["Siege"] == df["Siege"].max()].to_dict(orient="records")

    stats.append(f"Punkreichster Tag am {most_win[0]['Datum']} ({most_win[0]['Siege']})")
    stats.append(f"Siegreichster Tag am {most_win[0]['Datum']} ({most_win[0]['Siege']})")
    return stats