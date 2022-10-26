from flask import Flask


app: Flask = Flask(__name__)


@app.route("/")
def index() -> str:
    return "Index Page"


@app.route("/hello")
def hello() -> str:
    return "HELLo"


if __name__ == "__main__":
    app.run(debug=True)
