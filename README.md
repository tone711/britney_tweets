# britney_tweets
britney_tweets is a Flask and Mongodb app that allows searching the text of tweets from the Britney tweets dataset

## Installation

Pull this repository down locally

Data file - /data/britney_twitter_data.tsv

Replace the 5-line britney_twitter_data.tsv file with a larger file with the same format, if desired. Note the data file must be in the data folder and named, britney_twitter_data.tsv.

To run without modification a Docker installation is required. 

If you want to run it locally a MongoDB is required. To run locally, load a MongoDB named, britney_db, with a collection named, tweets.
Edit the MongoDBClient in the app.py file

```
    client = MongoClient(
                        host='localhost',
                        port=27017
                        #username='root',
                        #password='pass',
                        #authSource="admin"
                        )

```


## Running

run the command  docker-compose up

Wait a while for containers to build and Mongo DB to load data.

Open a browser to http://localhost:5000/

Enter the search criteria and select the search button.

View results!

## File Structure

│   app.py - main Python/Flask application

│   docker-compose.yml - Docker compose file

│   Dockerfile - Sets up Python application in Docker

│   README.md - this file

│   requirements.txt - required Python modules 


├─── /data/ - data to load into MongoDB

├────── britney_twitter_data.tsv  - tab-separated file of tweet data

├─── /data_import/ - MongoDB docker data load and initialization scripts

├────── create-index.js - called by data_import.sh, creates a MongoDB test index on the text field.

│────── data_import.sh - shell script that runs when the MongoDB docker container is initialized. Loads the .tsv file and creates an index.


├─── /templates/ - Flask HTML templates

├────── index.html - enter search value form

├────── result.html - display results



## Future Enhancements

Prettify HTML

Test suite

Convert places id to readable locations

Fix plot labels

Make DB more modular, less hardcoded paths
