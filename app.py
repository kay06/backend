from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Users table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable = False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Ticket table
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(255))
    description = db.Column(db.String(400))
    #status = db.Column(db.Integer) 

    def __init__(self, user_id, title, description):
        self.user_id = user_id
        self.title = title
        self.description = description

class TicketSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'title', 'description')


ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)

#new user sign up
@app.route('/new_user', methods=["POST"])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']


    new_user = User(name, email, password)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)

#user delete

#new ticket made
@app.route('/new_ticket', methods=["POST"])
def add_ticket():
    user_id = request.json['user_id']
    title = request.json['title']
    description = request.json['description'] 

    new_ticket = Ticket(user_id, title, description)

    db.session.add(new_ticket)
    db.session.commit()

    ticket = Ticket.query.get(new_ticket.id)

    return ticket_schema.jsonify(ticket)

#edit status

#remove ticket


if __name__ == '__main__':
    app.run(debug=True)