import os
from flask import Flask, session, redirect, url_for
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["AUTH_FLASK_SECRET_KEY"]

AUTH0_CALLBACK_URL = "http://brymck.io/callback"
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_CLIENT_SECRET = os.environ["AUTH0_CLIENT_SECRET"]
AUTH0_DOMAIN = "brymck.auth0.com"
AUTH0_BASE_URL = "https://brymck.auth0.com"
AUTH0_AUDIENCE = "http://brymck.io"

oauth = OAuth(app)
auth0 = oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=f"{AUTH0_BASE_URL}/oauth/token",
    authorize_url=f"{AUTH0_BASE_URL}/authorize",
    client_kwargs={
        "scope": "openid profile",
    },
)


# add the following endpoints underneath it
@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL,
                                    audience=AUTH0_AUDIENCE)


@app.route("/callback")
def callback():
    response = auth0.authorize_access_token()  # 1
    session["access_token"] = response["access_token"]  # 2
    userinfo_response = auth0.get("userinfo")  # 3
    userinfo = userinfo_response.json()
    session["user"] = userinfo["nickname"]  # 4
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    params = {"returnTo": url_for("front", _external=True),
              "client_id": AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + "/v2/logout?" + urlencode(params))


def get_forward_headers(request):
    headers = {}

    if "access_token" in session:
        headers["Authorization"] = "Bearer " + session["access_token"]

    # We handle other (non x-b3-***) headers manually
    if "user" in session:
        headers["end-user"] = session["user"]

    incoming_headers = ["x-request-id"]

    # Add user-agent to headers manually
    if "user-agent" in request.headers:
        headers["user-agent"] = request.headers.get("user-agent")

    for ihdr in incoming_headers:
        val = request.headers.get(ihdr)
        if val is not None:
            headers[ihdr] = val

    return headers


def serve():
    app.run(port=8080)


if __name__ == "__main__":
    serve()
