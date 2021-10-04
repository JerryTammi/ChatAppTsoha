from app import app
from flask import redirect, render_template, request, session
import users, threads, messages

@app.route('/', methods=["GET","POST"])
def index():
	list = threads.get_list_of_threads()
	id = users.user_id()
	if id == 0:
		return render_template("index.html", list_of_threads = list)
	else:
		user = users.get_username(id)
		return render_template("index.html", list_of_threads = list, username = user)
	

@app.route('/login', methods=["GET","POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	else:
		username = request.form.get("username")
		password = request.form.get("password")
		if not username or not password:
			error_statement = "All form fields required"
			return render_template("login.html",
			 error_statement = error_statement,
			 username = username)
		if users.login(username, password):
			list = threads.get_list_of_threads()
			return render_template("index.html", list_of_threads = list)
		else:
			error_statement = "Username and password don't match!"
			return render_template("login.html",
			 error_statement = error_statement,
			 username = username)
		return render_template("login.html")


@app.route('/register')
def register():
	return render_template("register.html")

@app.route('/accountcreated', methods=["POST", "GET"])
def accountcreated():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		username = request.form.get("username")
		password1 = request.form.get("password1")
		password2 = request.form.get("password2")
		is_admin = 'is_admin' in request.form
		print(is_admin)
		if not username or not password1 or not password2:
			error_statement = "All form fields required"
			return render_template("register.html",
			 error_statement = error_statement,
			 username = username)
		if len(username) > 50:
			error_statement = "Username is too long"
			return render_template("register.html",
			 error_statement = error_statement,
			 username = username)
		if password1 != password2:
			error_statement = "Passwords do not match!"
			return render_template("register.html",
			 error_statement = error_statement,
			 username = username)
		if len(password1) < 7:
			error_statement = "Password is too short!"
			return render_template("register.html",
			 error_statement = error_statement,
			 username = username)
		if users.register(username, password1, is_admin):
			return render_template("accountcreated.html", username = username)
		else:
			error_statement = "Username is taken!"
			return render_template("register.html",
			 error_statement = error_statement)
	

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/logout')
def logout():
	id = users.user_id()
	if id == 0:
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	users.logout()
	return render_template("logout.html")

@app.route('/thread/<int:id>', methods=["POST", "GET"])
def thread(id):
	if not threads.does_thread_exist(id):
		error_statement = "Thread does not exist"
		return default_homepage_with_error(error_statement)
	thread_details = threads.get_thread_details(id)
	list = messages.get_list(id)
	if not threads.does_thread_exist(id):
		error_statement = "Thread not found"
		return default_homepage_with_error(error_statement)
	else:
		return render_template("thread.html", id=id, messages=list, thread_details = thread_details)

@app.route('/threadcreated', methods=["POST", "GET"])
def threadcreated():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		title = request.form.get("threadtitle")
		if not title:
			error_statement = "Title required"
			return default_homepage_with_error(error_statement)
		if len(title) > 200:
			error_statement = "Title is too long"
			return default_homepage_with_error(error_statement)
		id = threads.new_thread(title)
		if not id:
			error_statement = "Something went wrong..."
			return default_homepage_with_error(error_statement)
		else:
			return redirect("thread/" + str(id))

@app.route("/send", methods=["POST", "GET"])
def send():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		content = request.form.get("content")
		id = request.form.get("id")
		if not messages.new_message(content, id):
			error_statement = "Something went wrong..."
			return default_homepage_with_error(error_statement)
		else:
			return redirect("thread/" + str(id))
	
def default_homepage_with_error(error_statement):
	list = threads.get_list_of_threads()
	id = users.user_id()
	if id == 0:
		return render_template("index.html", list_of_threads = list, error_statement = error_statement)
	else:
		user = users.get_username(id)
		return render_template("index.html", list_of_threads = list, username = user, 
			error_statement = error_statement)