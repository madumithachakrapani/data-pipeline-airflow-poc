import pandas as pd


def build_report(spotify_raw_extract):
    song_df = pd.DataFrame(spotify_raw_extract["songs"])
    #song_df = song_df[["artist_name"]].groupby(["artist_name"]).size()
    #print(song_df)
    song_df.to_csv("spotify_report.csv", sep='\t', encoding='utf-8')
