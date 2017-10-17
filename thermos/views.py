from flask import flash, render_template, redirect, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from thermos import app, db, login_manager
from forms import BookmarkForm, LoginForm, SignupForm
from models import User, Bookmark

# # Fake login
# def logged_in_user():
# 	return User.query.filter_by(username="wholebear").first()

@login_manager.user_loader
def lead_user(userid):
	return User.query.get(int(userid))

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', new_bookmarks=Bookmark.newest(5))

@app.route('/user/<username>')		# the <> passes the argument to the view function
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	form = BookmarkForm()					# On a GET request, the fields are empty and the form variables are also empty. On a POST request, the variables are full. This will likely only work because the action was "", as that means it referring to a still available form to read the values of
	if form.validate_on_submit():			# This line also checks to make sure the method is not GET
		url = form.url.data
		description = form.description.data
		bm = Bookmark(user=current_user, url=url, description=description)
		db.session.add(bm)
		db.session.commit()
		flash("Stored '{}'".format(bm.description))
		return redirect(url_for('index'))
	return render_template('bookmark_form.html', form=form, title="Add a bookmark")  # form=form is sent because the template is actually using the form to populate the DOM with form fields

@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
	bookmark = Bookmark.query.get_or_404(bookmark_id)
	if current_user != bookmark.user:
		abort(403)
	form = BookmarkForm(obj=bookmark)					# On a GET request, the fields are empty and the form variables are also empty. On a POST request, the variables are full. This will likely only work because the action was "", as that means it referring to a still available form to read the values of
	if form.validate_on_submit():			# This line also checks to make sure the method is not GET
		form.populate_obj(bookmark)
		db.session.commit()
		flash("Stored '{}'".format(bookmark.description))
		return redirect(url_for('user', username=current_user.username))
	return render_template('bookmark_form.html', form=form, title="Edit Bookmark")  # form=form is sent because the template is actually using the form to populate the DOM with form fields

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		# login and validate the user
		# user = User.query.filter_by(username=form.username.data).first() #(old way)
		user = User.get_by_username(form.username.data)
		if user is not None and user.check_password(form.password.data):
			login_user(user, form.remember_me.data)
			flash("Logged in successfully as {}.".format(user.username))
			return redirect(request.args.get('next') or url_for('user', username=user.username))
		flash('Incorrect username or password.')
	return render_template("login.html", form=form)

@app.route("/logout")
def logout():
	logout_user()	
	return redirect(url_for('index'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		user = User(email=form.email.data, 
			username=form.username.data, 
			password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Welcome, {}! Please login.".format(user.username))
		return redirect(url_for("login"))
	return render_template("signup.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
	return render_template('500.html'), 500
