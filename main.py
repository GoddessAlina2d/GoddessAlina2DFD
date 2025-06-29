import os
import random
from flask import Flask, redirect, request, session, url_for
from requests_oauthlib import OAuth1Session



app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_dev_secret")





# Twitter API credentials
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
CALLBACK_URL = os.getenv("CALLBACK_URL", "https://goddessalina2d.onrender.com/callback")

# OAuth endpoints
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

@app.route("/")
def index():
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, callback_uri=CALLBACK_URL)
    fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL)
    session['resource_owner_key'] = fetch_response.get('oauth_token')
    session['resource_owner_secret'] = fetch_response.get('oauth_token_secret')

    return redirect(oauth.authorization_url(AUTHENTICATE_URL))

@app.route("/callback")
def callback():
    if 'resource_owner_key' not in session or 'resource_owner_secret' not in session:
        return "Session expired or invalid. Please go back to the homepage and try again.", 400

    verifier = request.args.get('oauth_verifier')
    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=session['resource_owner_key'],
        resource_owner_secret=session['resource_owner_secret'],
        verifier=verifier
    )
    tokens = oauth.fetch_access_token(ACCESS_TOKEN_URL)
    session['access_token'] = tokens['oauth_token']
    session['access_token_secret'] = tokens['oauth_token_secret']
    return redirect(url_for('update_profile'))




@app.route("/update_profile")
def update_profile():
    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=session['access_token'],
        resource_owner_secret=session['access_token_secret']
    )

    # Update profile name & bio
    random_suffix = f"{random.randint(0, 9999):04}"  # Ensures 4 digits
    new_name = f"Goddess Alina's simp #{random_suffix}"

    profile_resp = oauth.post(
        "https://api.twitter.com/1.1/account/update_profile.json",
        data={"name": new_name, "description": "I'm @GoddessAlina2D's *click* bot now, join me in her herd of bots https://GoddeessAlina2D.com . Send to Goddess youpay.me/GoddessAlina2D", "location": "*click* send *click* send", "url": "beacons.ai/GoddessAlina2D"}
    )
    print("Profile update:", profile_resp.status_code, profile_resp.text)

    # Update profile image
    with open("Profile (1) (1).png", "rb") as img:
        oauth.post("https://api.twitter.com/1.1/account/update_profile_image.json", files={"image": img})

    # Update banner
    with open("Banner.png", "rb") as banner:
        oauth.post("https://api.twitter.com/1.1/account/update_profile_banner.json", files={"banner": banner})

     

    return redirect("https://ctt.ac/REct3")
    

    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

