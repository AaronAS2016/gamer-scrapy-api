from flask import Flask
app =  Flask(__name__)

@app.route("/")
def test_route():
    pass