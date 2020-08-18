from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.model import User, Post, PostComment, UserModel
from flask_blog.posts.forms import PostForm, CommentForm
from flask_blog.models.forms import ModelForm, TestModel_Image, TestModel_CSV, TempModel
from flask_blog.users.utils import save_model, save_model_test_picture
# from flask_blog.dockerpy import create_container

models = Blueprint('models', __name__)

@models.route("/model/<int:model_id>", methods=['POST','GET'])
def model(model_id):
	model = UserModel.query.get_or_404(model_id)
		
	return render_template('model.html', title=model.name, model=model)

@login_required
@models.route("/create_model", methods=['POST','GET'])
def create_model():
	form = ModelForm()
	if form.validate_on_submit():

		model_code, f_nm_code = save_model(form.model_code.data)
		model_test, f_nm_test = save_model(form.model_test.data)
		model_hdf5, f_nm_hdf5 = save_model(form.model_hdf5.data)

		#########################################

		# create_container()

		#########################################

		model = UserModel(name=form.name.data, 
						  description=form.description.data,
						  model_code=model_code,
						  model_test=model_test,
						  model_hdf5=model_hdf5,
						  price=form.price.data,
						  validation_datatype=form.validation_datatype.data,
						  model_author=current_user)
		db.session.add(model)

		db.session.commit()
		flash('Your Model has been Uploaded!', 'success')
		return redirect(url_for('users.account'))
	return render_template('create_model.html', form = form)


import os
import importlib
import sys
@login_required
@models.route("/test_model/<int:model_id>", methods=['POST', 'GET'])
def test_model(model_id):
	model = UserModel.query.get_or_404(model_id)
	try:
		if model.validation_datatype == 'image':
			form1 = TestModel_Image()
			if form1.validate_on_submit():
				if form1.test_file.data:
					picture_file = save_model_test_picture(form1.test_file.data)
				static_path = "E:/Virtual Envs/Environments/Flask_ver0/flask_blog/static/models/"
				pic_path = "E:/Virtual Envs/Environments/Flask_ver0/flask_blog/static/model_test_pics/"

				model_test_file = model.model_test
				model_hdf5_file = model.model_hdf5

				# print(type(model_test_file)) - string
				hdfd_path = os.path.join(static_path,model_hdf5_file)
				test_file_path = os.path.join(static_path,model_test_file)
				image_path = os.path.join(pic_path, picture_file)
				print(test_file_path)
				# module = __import__(test_file_path)

				spec = importlib.util.spec_from_file_location('module', test_file_path)
				module = importlib.util.module_from_spec(spec)
				sys.modules[spec.name] = module 
				spec.loader.exec_module(module)

				print("ModuleImported!")
				result = module.model_pred(hdfd_path, image_path)

				flash(str(result), 'success')
			return render_template('test_model.html', form=form1, model=model)
		else:
			form1 = TestModel_CSV()
			return render_template('test_model.html', form=form1, model=model)
	except:
		return render_template('errors/500.html')
		
	