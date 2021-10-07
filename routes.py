from app import app
from flask import redirect, render_template, request, session
import users, threads, messages, thread_subsections

@app.route("/", methods=["GET","POST"])
def index():
	list = threads.get_list_of_threads()
	subsections = thread_subsections.get_list_of_subsections()
	id = users.user_id()
	if id == 0:
		return render_template("index.html", list_of_threads = list, subsections = subsections)
	else:
		user = users.get_username(id)
		admin = users.check_if_admin(id)
		return render_template("index.html", list_of_threads = list, username = user, admin = admin, subsections = subsections)
	

@app.route("/login", methods=["GET","POST"])
def login():
	if request.method == "GET":
		id = users.user_id()
		if id != 0:
			error_statement = "Already logged in"
			return default_homepage_with_error(error_statement)
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
			admin = users.check_if_admin(users.user_id())
			subsections = thread_subsections.get_list_of_subsections()
			return render_template("index.html", list_of_threads = list, admin = admin, subsections = subsections)
		else:
			error_statement = "Username and password don't match!"
			return render_template("login.html",
			 error_statement = error_statement,
			 username = username)


@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/accountcreated", methods=["POST", "GET"])
def accountcreated():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		username = request.form.get("username")
		password1 = request.form.get("password1")
		password2 = request.form.get("password2")
		is_admin = 'is_admin' in request.form
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
		if len(password1) < 4:
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
	

@app.route("/about")
def about():
	id = users.user_id()
	if id == 0:
		return render_template("about.html")
	admin = users.check_if_admin(users.user_id())
	return render_template("about.html", admin = admin)

@app.route("/logout")
def logout():
	id = users.user_id()
	if id == 0:
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	users.logout()
	return render_template("logout.html")

@app.route("/thread/<int:id>", methods=["POST", "GET"])
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
		user_id = users.user_id()
		if user_id == 0:
			return render_template("thread.html", id=id, messages=list, thread_details = thread_details)
		admin = users.check_if_admin(user_id)
		return render_template("thread.html", id=id, messages=list, thread_details = thread_details, admin = admin)

@app.route("/threadcreated", methods=["POST", "GET"])
def threadcreated():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		title = request.form.get("title")
		subsection_id = request.form.get("subsection_id")
		if not title:
			error_statement = "Title required"
			return default_homepage_with_error(error_statement)
		if len(title) > 200:
			error_statement = "Title is too long"
			return default_homepage_with_error(error_statement)
		thread_id = threads.new_thread(title, subsection_id)
		if not thread_id:
			error_statement = "Something went wrong..."
			return default_homepage_with_error(error_statement)
		else:
			return redirect("thread/" + str(thread_id))

@app.route("/send", methods=["POST", "GET"])
def send():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		content = request.form.get("content")
		id = request.form.get("id")
		if len(content) == 0:
			return redirect("thread/" + str(id))
		if len(content) > 5000:
			return redirect("thread/" + str(id))
		if not messages.new_message(content, id):
			error_statement = "Something went wrong..."
			return default_homepage_with_error(error_statement)
		else:
			return redirect("thread/" + str(id))

@app.route("/admin")
def admin():
	if not users.check_if_admin(users.user_id()):
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	return render_template("admin.html")

@app.route("/admin/subsection", methods=["POST", "GET"])
def subsection():
	user_id = users.user_id()
	admin = users.check_if_admin(user_id)
	if user_id == 0 or not admin:
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	if request.method == "GET":
		list = thread_subsections.get_list_of_subsections()
		return render_template("subsection.html", list = list, admin = admin)
	if request.method == "POST":
		title = request.form.get("title")
		if not title:
			return redirect("/subsection")
		if len(title) > 50:
			return redirect("/subsection")
		thread_subsections.new_subsection(title)
		return redirect("/subsection")

@app.route("/submit", methods=["POST", "GET"])
def submit():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		subsection_id = request.form.get("subsection_id")
		return render_template("submit.html", subsection_id = subsection_id)

@app.route("/deletemessage", methods=["POST", "GET"])
def deletemessage():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		message_id = request.form.get("message_id")
		thread_id = request.form.get("thread_id")
		messages.delete_message(message_id)
		return redirect("thread/" + str(thread_id))

@app.route("/editmessage", methods=["POST", "GET"])
def editmessage():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		message_id = request.form.get("message_id")
		thread_id = request.form.get("thread_id")
		content = request.form.get("editmessage_content")
		if not content:
			return redirect("thread/" + str(thread_id))
		messages.edit_message(message_id, content)
		return redirect("thread/" + str(thread_id))

@app.route("/deletethread", methods=["POST", "GET"])
def deletethread():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		thread_id = request.form.get("thread_id")
		threads.delete_thread(thread_id)
		return redirect("/")

@app.route("/admin/users")
def admin_user_page():
	id = users.user_id()
	if id == 0 or not users.check_if_admin(id):
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	else:
		list = users.get_list_of_users()
		return render_template("adminusers.html", users = list)

@app.route("/search", methods=["POST", "GET"])
def search():
	search_content = request.form.get("search_content")
	if not search_content:
		return redirect("/")

def default_homepage_with_error(error_statement):
	list = threads.get_list_of_threads()
	subsections = thread_subsections.get_list_of_subsections()
	id = users.user_id()
	if id == 0:
		return render_template("index.html", list_of_threads = list, error_statement = error_statement, subsections = subsections)
	else:
		user = users.get_username(id)
		admin = users.check_if_admin(id)
		return render_template("index.html", list_of_threads = list, username = user, 
			error_statement = error_statement, admin = admin, subsections = subsections)

