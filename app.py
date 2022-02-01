from flask import Flask as fl
from flask import render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = fl(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://zkukfDYFBH:UU1CktdOHK@remotemysql.com/zkukfDYFBH'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class user(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    name = db.Column(db.String)
    age = db.Column(db.Integer)

    def __repr__(self):
        return "name: " + self.name + " id: " + str(self.id) + " age: " + str(self.age)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/DBTest")
def DBTest():
    all = user.query.all()
    return str(all)

if __name__ == "__main__":
    #db.create_all()
    #admin = User(id=50400, name="adaadadadadadadadadd", age="234226")
    #guest = User(id=6000, name="Patwdwewerich", age="483")
    #db.session.add(admin)
    #db.session.add(guest)
    #db.session.commit()
    app.run(debug=True)
    


#Username: zkukfDYFBH
#Database name: zkukfDYFBH
#Password: UU1CktdOHK
#Server: remotemysql.com
#Port: 3306


#class User(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
 #   name = db.Column(db.String(80), unique=True, nullable=False)
 #   age = db.Column(db.Integer, unique=True, nullable=False)
  #  #varchar(100)
    #age #int(11)
  #  def __repr__(self):
   #     return "User"