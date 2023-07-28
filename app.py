import os
from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    message = Column(String, index=True)


# Create the table in the database
Base.metadata.create_all(bind=engine)


@app.route('/messages', methods=['POST'])
def add_message():
    data = request.get_json()

    name = data['name']
    email = data['email']
    message = data['message']

    new_message = Message(name=name, email=email, message=message)

    db = SessionLocal()
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    db.close()
    return new_message


if __name__ == '__main__':
    app.run(host='0.0.0.0')
