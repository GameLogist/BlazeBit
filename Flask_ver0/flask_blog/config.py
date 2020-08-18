import os

class Config:
	SECRET_KEY = '3354545f147ed145b8aa308a8baa9eab'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'ayush.tiwari.main@gmail.com'
	MAIL_PASSWORD = '9793033765'