import collections as coll
import json
from pathlib import Path
import pandas as pd
import numpy as np

def create_match_statistic(player=None, pivot=False):
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
        if row["win"] == "player_one":
            return row["player_one"]
        return row["player_two"]


    df["Spieler"] = df.apply(get_winner, axis=1)

    df = df.groupby(by=["date", "Spieler"]).size().reset_index(name="Siege")
    df = df.rename(columns={"date": "Datum"})
    df = df.sort_values(by=["Datum", "Siege"], ascending=False).reset_index(drop=True)

    if player:
        df = df.loc[df["Spieler"] == player]
    
    if pivot:
        with open("./spieler.json") as f:
            players = json.loads(f.read())
        df = df.pivot(index="Datum", columns="Spieler", values="Siege")
        
        for pl in players:
            if pl not in df:
                df[pl] = np.nan
                
        return df.fillna(0)
    return df