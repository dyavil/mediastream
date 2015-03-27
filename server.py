from flask import Flask
import sqlalchemy
from sqlalchemy import and_
from flask import app, request, session,redirect
from flask.ext.login import LoginManager, login_user, logout_user
from flask import render_template
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from bddorm import User, Base, Media, Section, Comment
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import string
import json
import hashlib
import random

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def start():
	ses = create_session()
	for instance in ses.query(User).order_by(User.id): 
		print instance.username, instance.email
	return render_template('home.html')

@app.route('/signup', methods=['POST'])
def sign_up():
	email = request.form['email']
	pseudo = request.form['pseudo']
	password = request.form['password']
	token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
	m = hashlib.md5()
	m.update(password)
	pwd = m.hexdigest()
	ses = create_session()
	newUser = User(pseudo, pwd, email, token)
	ses.add(newUser)
	ses.commit()
	login_user(newUser)
	return redirect('/')

@app.route('/signin', methods=['POST'])
def sign_in():	
	pseudo = request.form['username']
	password = request.form['passwordlog']
	token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))	
	print password
	m = hashlib.md5()
	m.update(password)
	print m.hexdigest()
	pwd = m.hexdigest()
	ses = create_session()
	user = None
	try: 
		user = ses.query(User).filter(and_(User.password == pwd, User.username == pseudo)).one()
	except NoResultFound, e:
		print e
		return json.dumps({'success': False, 'message':'Wrong username/password'})
	login_user(user)
	return redirect('/')

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')	

def create_session():
    engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/seedbox')
    Session = sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}
    return session

@login_manager.user_loader
def load_user(userid):
	ses = create_session()
	for user in ses.query(User).\
			filter(User.id==userid): 
		return user
	return None


app.secret_key = '8c1e6be096d4a75d31802c564783badd'

if __name__ == '__main__':
	app.debug = True
	app.run()