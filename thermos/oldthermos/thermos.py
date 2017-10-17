import os
# from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bookmarks = []
app.config['SECRET_KEY'] = '\xb8m\xa0X\x7fRJ\xdd]\xcb\x13\x8be\xad0\xb4@\xca\xdd|\xe7\xc3\x02\xda'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
db = SQLAlchemy(app)

from forms import BookmarkForm
# from models import Bookmark
import models

# Fake login
def logged_in_user():
	return models.User.query.filter_by(username="wholebear").first()


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', new_bookmarks=models.Bookmark.newest(5))


@app.route('/add', methods=['GET', 'POST'])
def add():
	form = BookmarkForm()					# On a GET request, the fields are empty and the form variables are also empty. On a POST request, the variables are full. This will likely only work because the action was "", as that means it referring to a still available form to read the values of
	if form.validate_on_submit():			# This line also checks to make sure the method is not GET
		url = form.url.data
		description = form.description.data
		bm = models.Bookmark(user=logged_in_user(), url=url, description=description)
		db.session.add(bm)
		db.session.commit()
		flash("Stored '{}'".format(description))
		return redirect(url_for('index'))
	return render_template('add.html', form=form)  # form=form is sent because the template is actually using the form to populate the DOM with form fields

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
	return render_template('500.html'), 500


# if __name__ == '__main__':		# This was commented out because of manage.py and runserver
	# app.run()
	# app.run(debug = True)


# def store_bookmark(url, description):
# 	bookmarks.append(dict(
# 		url = url,
# 		description=description,
# 		user = "wholebear",
# 		date = datetime.utcnow()
# 	))

# def new_bookmarks(num):
# 	return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


# @app.route('/add', methods=['GET', 'POST'])
# def add():
# 	if request.method == "POST":
# 		url = request.form['url']
# 		store_bookmark(url)
# 		flash("Stored bookmark '{}'".format(url))
# 		return redirect(url_for('index'))
# 	return render_template('add.html')


# @app.route('/add', methods=['GET', 'POST'])
# def add():
# 	form = BookmarkForm()					# On a GET request, the fields are empty and the form variables are also empty. On a POST request, the variables are full. This will likely only work because the action was "", as that means it referring to a still available form to read the values of
# 	if form.validate_on_submit():			# This line also checks to make sure the method is not GET
# 		url = form.url.data
# 		description = form.description.data
# 		store_bookmark(url, description)
# 		flash("Stored '{}'".format(description))
# 		return redirect(url_for('index'))
# 	return render_template('add.html', form=form)  # form=form is sent because the template is actually using the form to populate the DOM with form fields
