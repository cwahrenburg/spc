from flask import Flask

app = Flask(__name__)

@app.route("/")
def helloWorld():
    return "<p>Hello, World!<p>"

@app.route('/test/')
def test():
    return "The test page"

@app.route('/about')
def about():
    return "the about page"
