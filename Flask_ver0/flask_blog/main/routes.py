from flask import render_template, request, redirect, Blueprint, send_from_directory
from flask_blog.model import Post
from flask import url_for, current_app
import os
import speech_recognition as sr  
import datetime

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts)

@main.route("/about")
def about():
	return render_template('about.html', title='About')

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/png')

@main.route("/speech")
def speech():
	r = sr.Recognizer()                                                                                   
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		print("Speak:")
		audio = r.listen(source, timeout=5)   
	
	result =r.recognize_google(audio)

	if result.lower() == "login":
		return redirect(url_for('users.login'))
	elif result.lower() == "register":
		return redirect(url_for('users.register'))
	elif result.lower() == "about":
		return redirect(url_for('main.about'))
	elif result.lower() == "home":
		return redirect(url_for('main.home'))
	elif result.lower() == "logout":
		return redirect(url_for('users.logout'))
	elif result.lower() == "my account":
		return redirect(url_for('users.account'))
	else:
		return redirect(url_for('main.home'))