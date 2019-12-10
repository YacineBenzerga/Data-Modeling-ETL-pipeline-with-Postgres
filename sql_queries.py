# Create tables

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id INT PRIMARY KEY,
        start_time TIMESTAMP NOT NULL,
        user_id INT NOT NULL REFERENCES users (user_id),
        level VARCHAR,
        song_id VARCHAR REFERENCES songs (song_id),
        artist_id VARCHAR REFERENCES artists (artist_id),
        session_id INT NOT NULL,
        location VARCHAR,
        user_agent VARCHAR
    )""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    gender CHAR(1),
    level VARCHAR NOT NULL
)""")


song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    artist_id VARCHAR NOT NULL REFERENCES artists (artist_id),
    year INT NOT NULL,
    duration NUMERIC NOT NULL)""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR PRIMARY KEY,
    artist_name VARCHAR,
    artist_location VARCHAR,
    artist_latitude NUMERIC,
    artist_longitude NUMERIC)""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP NOT NULL PRIMARY KEY,
        hour NUMERIC NOT NULL,
        day NUMERIC NOT NULL,
        week NUMERIC NOT NULL,
        month NUMERIC NOT NULL,
        year NUMERIC NOT NULL,
        weekday NUMERIC NOT NULL
    )
""")

# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"


# INSERT DATA INTO TABLES

song_table_insert = (
    """INSERT INTO songs (song_id,title,artist_id,year,duration) VALUES (%s,%s,%s,%s,%s)""")

artist_table_insert = (
    """INSERT INTO artists (artist_id,artist_name,artist_location,artist_latitude,artist_longitude) VALUES (%s,%s,%s,%s,%s)""")


time_table_insert = ("""
    INSERT INTO time (
        start_time,
        hour,
        day,
        week,
        month,
        year,
        weekday
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time)
    DO NOTHING
""")

user_table_insert = (
    """
    INSERT into users (
        user_id,
        first_name,
        last_name,
        gender,
        level
    ) VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id)
    DO UPDATE
        SET level = EXCLUDED.level
    """
)

song_select = ("""
    SELECT 
        songs.song_id AS song_id,
        songs.artist_id AS artist_id
    FROM
        songs
        JOIN artists ON (songs.artist_id = artists.artist_id)
    WHERE
        songs.title = %s AND 
        artists.name = %s AND 
        songs.duration = %s
""")

create_tbl_queries = [time_table_create, user_table_create,
                      artist_table_create, song_table_create, songplay_table_create]
drop_tbl_queries = [songplay_table_drop, user_table_drop,
                    song_table_drop, artist_table_drop, time_table_drop]
