from app import db
from app import app
from hashlib import md5

import sys
if sys.version_info >= (3,0):
	enable_search = False
else:
	enable_search = True
	import flask.ext.whooshalchemy as whooshalchemy

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index= True, unique= True)
	email = db.Column(db.String(120), index = True, unique = True)
	ideas = db.relationship('Idea', backref = 'author', lazy = 'dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	def user_ideas(self):
		return Idea.query.filter(id > 0)

	def avatar(self, size):
		return '/static/img/%s.jpg' %(self.id)
		#return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' %(md5(self.email.encode('utf-8')).hexdigest(), size)

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname=nickname).first() is None:
			return nickname
		version = 2
		while True:
			new_nickname = nickname + str(version)
			if User.query.filter_by(nickname=new_nickname).first() is None:
				break
			version += 1
		return new_nickname

	def __repr__(self):
		return '<User %r>' % (self.nickname)

class Idea(db.Model):
	__searchable__ = ['description']

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(120), index = True, unique = True)
	description = db.Column(db.String(1000))
	rank = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Idea %r>' % (self.description)

if enable_search:
	whooshalchemy.whoosh_index(app, Idea)