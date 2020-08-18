import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_ , f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
	
	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

def save_model_test_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_ , f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/model_test_pics', picture_fn)
	
	output_size = (200,200)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

def save_model(form_model):
	random_hex = secrets.token_hex(8)
	f_nm , f_ext = os.path.splitext(form_model.filename)
	model_fn = random_hex + f_ext
	model_path = os.path.join(current_app.root_path, 'static/models', model_fn)
	
	form_model.save(model_path)

	return model_fn, f_nm

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
				  sender='ayush.tiwari410@gmail.com',
				  recipients=[user.email])
	msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request simply ignore this request.
"""
	mail.send(msg)