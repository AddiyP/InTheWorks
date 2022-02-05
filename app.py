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

class event(db.Model):
    __tablename__ = "events"
    EventId = db.Column(db.Integer, primary_key = True, nullable=False)
    EventName = db.Column(db.String, primary_key = False, nullable=False)
    Description = db.Column(db.String, primary_key = False, nullable=False)
    CreatorId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    RegionId = db.Column(db.Integer, db.ForeignKey('regions.RegionId'))
    def __repr__(self):
        return "id: " + str(self.EventId) + " EventName: " + str(self.EventName) + " Description: " + str(self.Description) + " CreatorId: " + str(self.CreatorId) 
    
class regions(db.Model):
    __tablename__ = "regions"
    RegionId = db.Column( db.Integer, primary_key = True, nullable=False )
    Name = db.Column(db.String, nullable=False)
    def __repr__(self):
        return "id: " + str(self.RegionId) + " Name: " + str(self.Name)

@app.route("/", methods=["GET"])
def main():
    checkUserId = flask.request.args.get("userID")
    returnedUser = 0
    if checkUserId  is not None:
        returnedUser = checkUserId
    return render_template("main.html", setUserID = returnedUser)

@app.route("/DBTest")
def DBTest():
    all = user.query.all()
    return "<p>" + str(all) + "</p>" + "<p><a href=\"/\">Back to main</a></p>"

@app.route("/Signup")
def SignupPage():
    return render_template("signup.html")

@app.route("/SubmitEvent")
def submit_event():
    return render_template("submit_event.html")

@app.route("/EventSubmit", methods=['POST'])
def event_submit():
    name = flask.request.form["name"]
    description = flask.request.form["description"]
    creator_id = 1
    region_id = 1
    NewEvent = event(EventName=name, Description=description, CreatorId=creator_id, RegionId=region_id)
    db.session.add(NewEvent)
    db.session.commit()

    return flask.redirect(flask.url_for("main"))

@app.route("/SignupSubmit", methods=['POST'])
def SignupSubmit():
    inUsername = flask.request.form["username"]
    inEmail = flask.request.form["email"]

    NewUser = user(username=inUsername, email=inEmail)
    db.session.add(NewUser)
    db.session.commit()

    return flask.redirect(flask.url_for("main"))

@app.route("/SignInPage")
def sign_in_page():
    return render_template("sign_in.html");

@app.route("/SignIn", methods=["POST"])
def handle_sign_in():
    check = user.query.filter_by(username=flask.request.form["name"]).first()
    if check is None:
        return "USER NOT FOUND"
    return flask.redirect(flask.url_for("main", userID = check.id))

if __name__ == "__main__":
    db = initDatabase(app)
    app.run(debug=True)

#Username: zkukfDYFBH
#Database name: zkukfDYFBH
#Password: UU1CktdOHK
#Server: remotemysql.com
#Port: 3306