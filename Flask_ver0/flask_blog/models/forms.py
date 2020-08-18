from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField,SelectMultipleField, FloatField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ModelForm(FlaskForm):
	name = StringField('Title', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[DataRequired()])
	validation_datatype = SelectField('File Formats', choices = [('csv', 'CSV / TXT / DOCX'), ('image', 'JPEG / JPG / PNG')], validators=[DataRequired()])

	model_code = FileField('Upload Model Code', validators=[FileAllowed(['zip']), FileRequired()])
	model_test = FileField('Upload Model Test Code', validators=[FileAllowed(['py','js']), FileRequired()])
	model_hdf5 = FileField('Upload Model HDF5 File', validators=[FileAllowed(['h5']), FileRequired()])

	price = FloatField('Price', validators=[DataRequired()])

	submit = SubmitField('Post')

class TestModel_Image(FlaskForm):
	test_file = FileField('Upload Image File', validators=[FileAllowed(['jpeg','png','jpg']), FileRequired()])

	submit = SubmitField('Test')


class TestModel_CSV(FlaskForm):
	test_file = FileField('Upload Data File', validators=[FileAllowed(['csv','txt','docx']), FileRequired()])

	submit = SubmitField('Test')

class TempModel(FlaskForm):
	submit = SubmitField('Test')