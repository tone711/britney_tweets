'''Britney Tweets Searcher '''

# import modules
import base64
import io
from flask import Flask, request, render_template
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# make it a flask app
app = Flask(__name__)

def get_db():
    """ Return a mongodb client """
    client = MongoClient(
                        host='localhost',
                        port=27017,
                        username='root',
                        password='pass',
                        authSource="admin"
                        )
    db = client["britney_db"]
    return db

@app.route('/', methods =["GET"])
def brit_index():
    """ return the index home page"""
    return render_template('index.html')


@app.route('/result', methods =["POST"])
def brit_search():
    """ Query the MongoDn and return a panda dataframe(df) """
    """
    Answer the following:
    -	How many tweets were posted containing the term on each day?
    -	How many unique users posted a tweet containing the term?
    -	How many likes did tweets containing the term get, on average?
    -	Where (in terms of place IDs) did the tweets come from?
    -	What times of day were the tweets posted at? 
    -	Which user posted the most tweets containing the term?
    """

    # getting input with name = bsearch in HTML form
    search_value = request.form.get('bsearch')
    if search_value == '':
        return render_template('index.html')
    # get a dataframe from mongo query of search term
    df = get_britney_df(search_value)

    # clean some data
    # convert creaedt_at to datatime type
    df['created_at'] = pd.to_datetime(df['created_at'],
                                      infer_datetime_format=True,
                                      errors='coerce',
                                      utc=True)

    df['like_count'] = pd.to_numeric(df['like_count'], errors='coerce')

    # never used matplotlib before, but create a couple of charts
    plt.figure(1)
    fig, axs = plt.subplots(figsize=(12, 4))

    df.groupby(df['created_at'].dt.hour).size().plot(
        kind='bar', rot=0, ax=axs
    )
    axs.set_xlabel("Time of day (hours)", fontsize=12)
    axs.set_ylabel("Tweet Count", fontsize=12)
    axs.set_title('Tweet count by time of day', loc='left', y=0.85, x=0.02, fontsize='medium')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    hour_plot_url = base64.b64encode(img.getvalue()).decode()

    # tweet count by day
    plt.figure(2)
    figs, ax = plt.subplots(figsize=(12, 4))

    df.groupby(df['created_at'].dt.date).size().plot(
        kind='line', rot=0, ax=ax
    )
    ax.set_xlabel("Days", fontsize='medium')
    ax.set_ylabel("Tweet Count", fontsize='medium')
    ax.set_title('Tweet count by day', loc='left', y=0.85, x=0.02, fontsize='medium')
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    # set font and rotation for date tick labels
    plt.gcf().autofmt_xdate()


    img2 = io.BytesIO()
    plt.savefig(img2, format='png')
    img2.seek(0)

    day_plot_url = base64.b64encode(img2.getvalue()).decode()


    # TODO: use twarc2 and convert place ID to city names


    # pass the df and plots to results template
    return render_template('result.html',
                            brit_df=df,
                            hourplot=hour_plot_url,
                            dayplot=day_plot_url)


def get_britney_df(search_val: str):
    """get a dataframe based on search value"""
    try:
        db = get_db()

        # db.tweets.create_index( { "text": "text" } )
        # create text search query
        myquery = { "$text": { "$search": f"{search_val}" } }
        #myquery = { "text": { "$regex": f".*{search_val}*." } }
        # do query, returning used fields
        tweets = db.tweets.find(myquery,
                {"created_at":1, "author_handle":1,
                 "author_id":1, "like_count":1, "place_id":1, "text":1})
        df = pd.DataFrame(list(tweets))
        return df

    except:
        pass
    finally:
        if isinstance(db, MongoClient):
            db.close()

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
