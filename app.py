import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/messages', methods=['POST'])
def add_message():
    data = request.get_json()

    name = data['name']
    email = data['email']
    message = data['message']

    new_message = Message(name=name, email=email, message=message)

    try:
        db.session.add(new_message)
        db.session.commit()
        return jsonify({"message": "Message added successfully"}), 201
    except Exception as e:
        _ = e
        db.session.rollback()
        return jsonify({"message": "Failed to add message"}), 500
    finally:
        db.session.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
