db = connect( 'mongodb://localhost:27017/britney_db' );
db.tweets.createIndex({'text': 'text'});