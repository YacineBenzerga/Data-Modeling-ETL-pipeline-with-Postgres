# Data-Modeling-ETL-pipeline-with-Postgres

This project consists of creating a database schema and an ETL pipeline from a music streaming app collected data.  
The data resides in a directory of JSON logs containing user activity as well as JSON metadata on the songs.  


.
##file structure

├──run.sh

├──src

│   ├── create_tables.py

│   ├── etl.py

│   ├── sql_queries.py

├──input

│   ├── data

│       ├── log_data

│       ├── song_data


##Runing the ETL

-executing run.sh will run create_tables.py then etl.py

-create_tables.py: the creation of schema structure into the postgres database

-etl.py:main ETL process

-the JSON logs resides in the input directory

## Database Schema Design

### Song Plays table

- *Name:* `songplays`
- *Type:* Fact table

### Users table

- *Name:* `users`
- *Type:* Dimension table

### Songs table

- *Name:* `songs`
- *Type:* Dimension table

### Artists table

- *Name:* `artists`
- *Type:* Dimension table

### Time table

- *Name:* `time`
- *Type:* Dimension table


##How to run:
-Make the script executable with command chmod +x run.sh
-Run the script using ./run.sh
