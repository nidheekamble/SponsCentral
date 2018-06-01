from flask import Flask,render_template, url_for, flash, redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = "Three-lit-bulbs-ANSV"


@app.route("/")
@app.route("/home")
def home():
    return "<h1>Home Page</h1>"


@app.route("/about")
def about():
    return "<h1>About Page</h1>"


if __name__ == '__main__':
    app.run(debug=True)