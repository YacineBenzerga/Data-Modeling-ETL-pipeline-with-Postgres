import psycopg2
import pandas as pd
import os
import glob
from sql_queries import *
from create_tables import init_db_conn
import numpy as np


def get_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    return all_files


def df_processing(df):
    df = df.drop_duplicates()
    df = df.replace(np.nan, None, regex=True)
    return df


def insert_rows_from_df(cur, df_name, insert_query):
    for i, row in df_name.iterrows():
        try:
            cur.execute(insert_query, list(row))
        except psycopg2.Error as e:
            print("Error: Couldn't insert row")
            print(e)


def process_song_file(cur, filepath):
    # read json
    df = pd.read_json(filepath, lines=True)

    # Artist
    # process artist record
    artist_data = df[['artist_id', 'artist_name',
                      'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = df_processing(artist_data)
    # insert artist record
    insert_rows_from_df(cur, artist_data, artist_table_insert)

    # Song
    # process song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = df_processing(song_data)
    # insert song record
    insert_rows_from_df(cur, song_data, song_table_insert)


def process_log_file(cur, filepath):
    # read json
    df = pd.read_json(filepath, lines=True)
    df = df[df['page'] == 'NextSong']

    time_df = pd.DataFrame({
        'start_time': pd.to_datetime(df['ts'], unit='ms')
    })

    time_df['hour'] = time_df['start_time'].dt.hour
    time_df['day'] = time_df['start_time'].dt.day
    time_df['week'] = time_df['start_time'].dt.week
    time_df['month'] = time_df['start_time'].dt.month
    time_df['year'] = time_df['start_time'].dt.year
    time_df['weekday'] = time_df['start_time'].dt.weekday

    time_df = df_processing(time_df)

    insert_rows_from_df(cur, time_df, time_table_insert)

    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df = df_processing(user_df)
    user_df.columns = ['user_id', 'first_name', 'last_name', 'gender', 'level']
    insert_rows_from_df(cur, user_df, user_table_insert)

    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            index, pd.to_datetime(row.ts, unit='ms'),
            row.userId, row.level, songid, artistid,
            row.sessionId, row.location, row.userAgent
        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, fn):
    all_files = get_files(filepath)
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        fn(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    # Connect to the database
    cur, conn = init_db_conn("spokifydb")

    process_data(cur, conn, './input/data/song_data', process_song_file)
    process_data(cur, conn, './input/data/log_data', process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
