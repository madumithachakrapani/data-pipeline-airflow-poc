import pandas as pd
def transform_raw_data(spotify_raw_data):
    song_df = pd.DataFrame(spotify_raw_data["songs"])
    transformed_data = song_df[["artist_name"]].groupby(["artist_name"]).size()
    print(transformed_data)