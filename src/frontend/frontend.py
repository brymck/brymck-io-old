import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world!"

@app.route("/_healthz")
def health():
    return "ok"

if __name__ == "__main__":
    port = os.environ.get("PORT", "8080")
    app.run(port=port)
