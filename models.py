import os
from sqlalchemy import Column, String, Integer, create_engine, Table, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json

database_name = "blog"
database_path = "postgresql://zzfdfvvsacmkgd:8ad387f49ebe850ee26de882aca87e71cb5d1f9aeb0f6d78382813595006e5b7@ec2-34-203-114-67.compute-1.amazonaws.com:5432/dtcra685grbk5"
#database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()
#binds a flask application and a SQLAlchemy service

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Users(db.Model):  
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, autoincrement=True)
  #id = Column(Integer().with_variant(Integer, "postgresql"))
  full_name = Column(String)
  children = relationship("Posts")

  def __init__(self, full_name):
    self.full_name = full_name

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'full_name': self.full_name
    }



class Posts(db.Model):  
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  body = Column(String)
  author = Column(Integer, ForeignKey('users.id'))

  def __init__(self, title, body, author):
    self.title = title
    self.body = body
    self.author = author

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'body': self.body,
      'author': self.author 
    }

