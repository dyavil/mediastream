import os
import sys
import sqlalchemy
import datetime
from sqlalchemy import create_engine # connect to server
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/seedbox')

Base = declarative_base()


class User(Base):
	__tablename__ = 'boxusers'
	id = Column(Integer, primary_key=True)
	username = Column(String(80), nullable=False, primary_key=True)
	email = Column(String(80), nullable=False)
	name = Column(String(100), nullable=True)
	lastname = Column(String(100), nullable=True)
	picturepath = Column(String(250), nullable=True)
	password = Column(String(250), nullable=False)
	token = Column(String(250), nullable=False)
	signupdate = Column(DateTime, nullable=False)
	lastsginin = Column(DateTime, nullable=False)
	enabled = Column(Integer, nullable=True)
	medias = relationship("Media", backref='boxusers')
	sections = relationship("Section", backref='boxusers')
	comments = relationship("Comment", backref='boxusers')
	def __init__(self, username, password, email, tok):
		self.username = username
		self.password = password
		self.email = email
		self.token = tok
		self.signupdate = datetime.datetime.now()
		self.lastsginin = datetime.datetime.now()

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.username)


class Media(Base):
	__tablename__ = 'boxmedia'
	id = Column(Integer, primary_key=True)
	type = Column(String(20), nullable=False)
	userref = Column(Integer, ForeignKey('boxusers.id'))
	path = Column(String(250), nullable=True)
	name = Column(String(250), nullable=True)
	update = Column(DateTime, nullable=False)
	description = Column(Text, nullable=True)
	nbdl = Column(Integer, nullable=True)
	section = Column(Integer, ForeignKey('boxsection.id'))
	comments = relationship("Comment", backref='boxmedia')
	def __init__(self):
		self.update = datetime.datetime.now()


class Section(Base):
	__tablename__ = 'boxsection'
	id = Column(Integer, primary_key=True)
	userref = Column(Integer, ForeignKey('boxusers.id'))
	medias = relationship("Media", backref='boxsection')
	name = Column(String(250), nullable=True)
	description = Column(Text, nullable=True)
	path = Column(String(250), nullable=True)
	nbfiles = Column(Integer, nullable=True)


class Comment(Base):
	__tablename__ = 'boxcomment'
	id = Column(Integer, primary_key=True)
	userref = Column(Integer, ForeignKey('boxusers.id'))
	mediaref = Column(Integer, ForeignKey('boxmedia.id'))
	content = Column(Text, nullable=True)
	date = Column(DateTime, nullable=False)
	def __init__(self):
		self.date = datetime.datetime.now()



Base.metadata.create_all(engine)