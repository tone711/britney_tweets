#! /bin/bash loads the tsv file into mongodb
mongoimport --db=britney_db --collection=tweets --type=tsv --headerline --file='/src/data/britney_twitter_data.tsv'
mongosh --file /src/data_import/create-index.js

