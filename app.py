import tweepy
import os
from urllib.parse import urlparse

from flask import Flask, redirect, request, jsonify

app = Flask(__name__)

REDIRECT_URI = "https://83cf-2607-fa49-ad02-3000-484e-23ca-d67b-339e.ngrok-free.app/callback"

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=os.getenv("TWITTER_CLIENT_ID"),
    redirect_uri=REDIRECT_URI,
    scope=["tweet.read", "tweet.write", "users.read", "offline.access"],
    client_secret=os.getenv("TWITTER_CLIENT_SECRET"),
)

@app.route('/login')
def login():
    """
    Redirect the user to Twitter's authorization page.
    """

    url = oauth2_user_handler.get_authorization_url()

    print(url)

    return redirect(url)


@app.route('/callback')
def callback():
    """
    Handle the redirect from Twitter and extract the authorization code.
    """
    
    response = oauth2_user_handler.fetch_token(request.url.replace("http", "https", 1))

    access_token = response["access_token"]

    client = tweepy.Client(access_token)
    me = client.get_user(id="me")

    return jsonify({"me": me.data.__str__(), "tokens": response }), 200


@app.route('/me')
def me():
    client = tweepy.Client(os.getenv("ACCESS_TOKEN"))
    me = client.get_user(id="me")

    return jsonify({"me": me.data.__str__()}), 200

@app.route('/tweet', methods=['POST'])
def tweet():
    data = request.get_json()

    client = tweepy.Client(os.getenv("ACCESS_TOKEN"))
    tweet = client.create_tweet(text=data, user_auth=False)

    return jsonify({"tweet": tweet.data.__str__()}), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)