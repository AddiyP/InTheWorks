from flask import Flask as fl
import flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

def initDatabase(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://zkukfDYFBH:UU1CktdOHK@remotemysql.com/zkukfDYFBH'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    database = SQLAlchemy(app)
    return database

app = fl(__name__)
db = initDatabase(app)

class user(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    username = db.Column(db.String)
    email = db.Column(db.String)

    def __repr__(self):
        return "id: " + str(self.id) + " name: " + self.username + " email: " + str(self.email)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/DBTest")
def DBTest():
    all = user.query.all()
    return str(all)

@app.route("/Signup")
def SignupPage():
    return render_template("signup.html")

@app.route("/SignupSubmit", methods=['POST'])
def SignupSubmit():
    inUsername = flask.request.form["username"]
    inEmail = flask.request.form["email"]

    NewUser = user(username=inUsername, email=inEmail)
    db.session.add(NewUser)
    db.session.commit()

    return flask.redirect(flask.url_for("main"))

if __name__ == "__main__":
    db = initDatabase(app)
    app.run(debug=True)

#Username: zkukfDYFBH
#Database name: zkukfDYFBH
#Password: UU1CktdOHK
#Server: remotemysql.com
#Port: 3306