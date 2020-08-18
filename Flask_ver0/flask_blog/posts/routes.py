from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.model import User, Post, PostComment, UserModel
from flask_blog.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)

@posts.route("/posts/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title='New Post',
							form=form, legend='New Post')

@posts.route("/post/<int:post_id>", methods=['POST','GET'])
def post(post_id):
	post = Post.query.get_or_404(post_id)
	form = CommentForm()
	if form.validate_on_submit():
		comment = PostComment(content=form.content.data, comment_author=current_user, comment_post=post)
		db.session.add(comment)
		db.session.commit()
		flash('Your Comment has been submitted!', 'success')
		return redirect(url_for('posts.post', post_id=post.id))

	comments = PostComment.query.all()

	return render_template('post.html', title=post.title,comments=comments, post=post, form=form)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your Post has been Updated!', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post',
							form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))

@posts.route("/post/<int:post_id>/update_comment/<int:comment_id>", methods=['GET', 'POST'])
@login_required
def update_comment(comment_id, post_id):
	comment = PostComment.query.get_or_404(comment_id)
	post = Post.query.get_or_404(post_id)
	if comment.comment_author != current_user:
		abort(403)
	form = CommentForm()
	if form.validate_on_submit():
		comment.content = form.content.data
		db.session.commit()
		flash('Your Comment has been Updated!', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.content.data = comment.content
	comments = PostComment.query.all()
	return render_template('post.html',comments=comments, post=post, form=form)

@posts.route("/post/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
	comment = PostComment.query.get_or_404(comment_id)
	if comment.comment_author != current_user:
		abort(403)
	db.session.delete(comment)
	db.session.commit()
	flash('Your Comment has been deleted!', 'success')
	return redirect(url_for('main.home'))


