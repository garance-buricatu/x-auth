import tweepy
import os

from flask import Flask, redirect, request, jsonify

app = Flask(__name__)

REDIRECT_URI = "https://c599-2607-fa49-ad02-3000-4719-3fbf-dbe3-c303.ngrok-free.app/callback"

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=os.getenv("TWITTER_CLIENT_ID"),
    redirect_uri=REDIRECT_URI,
    scope=["tweet.read", "tweet.write", "users.read", "offline.access"],
    client_secret=os.getenv("TWITTER_CLIENT_SECRET"),
)

@app.route('/app/login')
def login_app():
    """
    Redirect the user to Twitter's authorization page.
    """

    oauth2_app_handler = tweepy.OAuth2AppHandler(
        consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
        consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
    )

    handler = oauth2_app_handler.apply_auth()

    return jsonify({"bearer_token": handler.bearer_token})

@app.route('/user/login')
def login_user():
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
    app.run(port=8080, debug=True)

# ngrok http http://localhost:8080
