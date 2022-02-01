from flask import Flask as fl
from flask import render_template

app = fl(__name__)

@app.route("/")
def main():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)