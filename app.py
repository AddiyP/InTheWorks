from flask import Flask as fl
import flask
from flask import render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import re

USERNAME_RE = re.compile(r'(\d|_|[a-z]|[A-Z]|-){3,20}')
EMAIL_RE = re.compile(r'\S+@\S+[.]\S+')

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
    lat = db.Column(db.Float, primary_key = False, nullable = False)
    lng = db.Column(db.Float, primary_key = False, nullable = False)
    def __repr__(self):
        return "id: " + str(self.EventId) + " EventName: " + str(self.EventName) + " Description: " + str(self.Description) + " CreatorId: " + str(self.CreatorId) 
    
class regions(db.Model):
    __tablename__ = "regions"
    RegionId = db.Column( db.Integer, primary_key = True, nullable=False )
    Name = db.Column(db.String, nullable=False)
    def __repr__(self):
        return "id: " + str(self.RegionId) + " Name: " + str(self.Name)

class user_interest(db.Model):
    __tablename__ = "user_interest"
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    event = db.Column(db.Integer, primary_key=False, nullable=False)
    user = db.Column(db.Integer, primary_key=False, nullable=False)
    def __repr__(self):
        return " " + str(self.user) + " has interest in " + str(self.event) + " "

@app.route("/", methods=["GET"])
def main_page():
    return render_template("main_page.html")

@app.route("/sign_up_handle", methods=['POST'])
def sign_up_handle():
    json_request = flask.request.get_json()
    req_username = json_request["username"]
    req_email = json_request["email"]
    check_name = user.query.filter_by(username=req_username).first()
    check_email = user.query.filter_by(email=req_email).first()
    err = "true"
    err_msg = ""

    username_success = USERNAME_RE.match(req_username)
    email_success = EMAIL_RE.match(req_email)
    check_success = check_name == None
    check_email_success = check_email == None

    new_user_id = 0

    if username_success != None and email_success != None and check_success and check_email_success:
        err = "false"
        new_user = user(username=req_username, email=req_email)
        db.session.add(new_user)
        db.session.flush() #like commit, but we can still access some values of new_user
        new_user_id = new_user.id
        db.session.commit()
    else:
        if username_success == None:
            err_msg += " USERNAME DOES NOT MATCH RE "
        if email_success == None:
            err_msg += " EMAIL DOES NOT MATCH RE "
        if not check_success:
            err_msg += " USERNAME ALREADY EXISTS "
        if not check_email_success:
            err_msg += " EMAIL ALREADY IN USE "
    
    return jsonify(error = err, user_id = new_user_id, error_message = err_msg, username = req_username)

@app.route("/sign_in_handle", methods=["POST"])
def sign_in_handle():
    json_request = flask.request.get_json()
    req_username = json_request["username"]
    check_name = user.query.filter_by(username=req_username).first()

    if check_name != None:
        checked_user_id = str(check_name.id)
        err = "false"
        err_msg = ""
    else:
        err_msg = " NO SUCH USER "
        err = "true"
        req_username = "null"
        checked_user_id = "0"
    return jsonify(error = err, user_id = checked_user_id, error_message = err_msg, username = req_username)

@app.route("/create_event_handle", methods=["POST"])
def create_event_handle():
    json_request = flask.request.get_json()
    req_name = json_request["name"]
    req_description = json_request["description"]
    if (len(req_description) < 1):
        req_description = "This event has no description."
    req_creator_id = json_request["creator_id"]
    req_region_id = 1
    req_lat = float(json_request["lat"])
    req_lng = float(json_request["lng"])
    check_exists = event.query.filter_by(EventName = req_name, Description = req_description).first()
    success_name = len(req_name) > 1 and len(req_name) < 30
    success_creator_id = int(req_creator_id) != 0

    err_msg = ""
    if check_exists is None and success_name and success_creator_id:
        new_event = event(EventName=req_name, Description=req_description, CreatorId=req_creator_id, RegionId=req_region_id, lat = req_lat, lng = req_lng)
        db.session.add(new_event)
        db.session.commit()
        err = "false"
    else:
        err = "true"
        if not success_name:
            err_msg += " INVALID NAME "
        if not success_creator_id:
            err_msg += " INVALID ID or MUST SIGN IN "
        if check_exists is not None:
            err_msg += " EVENT ALREADY EXISTS "

    return jsonify(error = err, error_message = err_msg)

@app.route("/get_events_handle", methods=["POST"])
def get_events_handle():
    returned_events = event.query.filter_by(RegionId = 1).all()
    added = False
    output = "{\"events\": ["
    for ev in returned_events:
        added = True
        creator_name = user.query.filter_by(id = ev.CreatorId).first().username
        event_interest = len(user_interest.query.filter_by(event=ev.EventId).all())
        output += "{\"name\":\""+ev.EventName+"\",\"description\":\""+ev.Description+"\",\"creator_name\":\""+creator_name+"\",\"lat\":\""+str(ev.lat)+"\",\"lng\":\""+str(ev.lng)+"\",\"event_id\":\""+str(ev.EventId)+"\", \"num_interest\":\""+str(event_interest)+"\"},"
    if added:
        output = output[:len(output) - 1]
    output += "]}"
    return output

@app.route("/show_interest", methods=["POST"])
def show_interest():
    json_request = flask.request.get_json()
    req_user = json_request["user_id"]
    req_event = json_request["event_id"]
    check = user_interest.query.filter_by(user=req_user, event=req_event).first()
    if check is not None or req_user is None:
        return jsonify()

    interest = user_interest(user=req_user, event=req_event)
    db.session.add(interest)
    db.session.commit()
    return jsonify();

if __name__ == "__main__":
    db = initDatabase(app)
    app.run(debug=True)

#Username: zkukfDYFBH
#Database name: zkukfDYFBH
#Password: UU1CktdOHK
#Server: remotemysql.com
#Port: 3306