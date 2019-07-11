
#import staements

import tweepy
from textblob import TextBlob
from flask import Flask,jsonify,request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# public private key

consumer_key = ''
consumer_secret = '2'
access_token = ''
access_token_secret = ''

#auth
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api=tweepy.API(auth)

@app.route('/',methods= ['POST'])
# main function
def sentimental_anlysis():
    values = request.get_json()
    if not values:
        response = { 'error' : 'no data found'}
        return jsonify(response),400
    word =  values['word']
    tweets=api.search(word)
    # main part giving value between -1 and 1 for polarity of sentiments, -1 being most negative
    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        pol=analysis.sentiment.polarity
        if pol>0.1:
            response = {'message':'postive','key_words':analysis.noun_phrases,'tweet':tweet.text}
            return jsonify(response),200
        else:
            response = {'message':'negative','key_words':analysis.noun_phrases,'tweet':tweet.text}
            return jsonify(response),200

if __name__ == '__main__':
    app.run(host = '0.0.0.0' , port = 5000)
