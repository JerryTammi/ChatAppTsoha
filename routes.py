from app import app
from flask import redirect, render_template, request, session
import users, threads, messages, thread_subsections, ban_appeals

@app.route("/")
def index():
	list = threads.get_list_of_threads()
	subsections = thread_subsections.get_list_of_subsections()
	user_id = users.user_id()
	if user_id == 0:
		return render_template("index.html", list_of_threads = list, subsections = subsections)
	if is_user_banned():
		return redirect("/banned")
	user = users.get_username(user_id)
	return render_template("index.html", list_of_threads = list, username = user, subsections = subsections)
	
@app.route("/login", methods=["GET","POST"])
def login():
	if request.method == "GET":
		id = users.user_id()
		if id != 0:
			error_statement = "Already logged in"
			return default_homepage_with_error(error_statement)
		return render_template("login.html")
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")
		if not username or not password:
			error_statement = "All form fields required"
			return render_template("login.html",
			 error_statement = error_statement,
			 username = username)
		if users.login(username, password):
			if is_user_banned():
				return redirect("/banned")
			return redirect("/")
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
	if request.method == "POST":
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
	user_id = users.user_id()
	if user_id == 0:
		return render_template("about.html")
	if is_user_banned():
		return redirect("/banned")
	return render_template("about.html")

@app.route("/logout")
def logout():
	user_id = users.user_id()
	if user_id == 0:
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	users.logout()
	return render_template("logout.html")

@app.route("/thread/<int:id>")
def thread(id):
	if is_user_banned():
		return redirect("/banned")
	if not threads.does_thread_exist(id):
		error_statement = "Thread does not exist"
		return default_homepage_with_error(error_statement)
	thread_details = threads.get_thread_details(id)
	list = messages.get_list(id)
	if not threads.does_thread_exist(id):
		error_statement = "Thread not found"
		return default_homepage_with_error(error_statement)
	user_id = users.user_id()
	return render_template("thread.html", id=id, messages=list, thread_details = thread_details)

@app.route("/threadcreated", methods=["POST", "GET"])
def threadcreated():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	if request.method == "POST":
		check_csrf()
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
	if request.method == "POST":
		check_csrf()
		content = request.form.get("content")
		thread_id = request.form.get("id")
		if len(content) == 0:
			return redirect("thread/" + str(thread_id))
		if len(content) > 1000:
			return redirect("thread/" + str(thread_id))
		if not messages.new_message(content, thread_id):
			error_statement = "Something went wrong..."
			return default_homepage_with_error(error_statement)
		else:
			return redirect("thread/" + str(thread_id))

@app.route("/admin")
def admin():
	if not users.check_if_admin(users.user_id()):
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	return render_template("admin.html")

@app.route("/admin/subsection", methods=["POST", "GET"])
def subsection():
	user_id = users.user_id()
	if user_id == 0 or not users.check_if_admin(user_id):
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	if request.method == "GET":
		list = thread_subsections.get_list_of_subsections()
		return render_template("subsection.html", list = list)
	if request.method == "POST":
		check_csrf()
		title = request.form.get("title")
		if not title:
			return redirect("/admin/subsection")
		if len(title) > 50:
			return redirect("/admin/subsection")
		thread_subsections.new_subsection(title)
		return redirect("/admin/subsection")

@app.route("/admin/subsection/delete", methods=["POST", "GET"])
def delete_subsection():
	user_id = users.user_id()
	if user_id == 0 or not users.check_if_admin(user_id) or request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	if request.method == "POST":
		check_csrf()
		subsection_id = request.form.get("subsection_id")
		if not subsection_id:
			return redirect("/admin/subsection")
		thread_subsections.delete_subsection(subsection_id)
		return redirect("/admin/subsection")

@app.route("/submit", methods=["POST", "GET"])
def submit():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	if request.method == "POST":
		check_csrf()
		subsection_id = request.form.get("subsection_id")
		return render_template("submit.html", subsection_id = subsection_id)

@app.route("/deletemessage", methods=["POST", "GET"])
def deletemessage():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	if request.method == "POST":
		check_csrf()
		message_id = request.form.get("message_id")
		thread_id = request.form.get("thread_id")
		messages.delete_message(message_id)
		return redirect("thread/" + str(thread_id))

@app.route("/editmessage", methods=["POST", "GET"])
def editmessage():
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	if request.method == "POST":
		check_csrf()
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
	if request.method == "POST":
		check_csrf()
		thread_id = request.form.get("thread_id")
		threads.delete_thread(thread_id)
		return redirect("/")

@app.route("/admin/users")
def admin_user_page():
	id = users.user_id()
	if id == 0 or not users.check_if_admin(id):
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	list = users.get_list_of_users()
	return render_template("adminusers.html", users = list, admin = users.check_if_admin(id))

@app.route("/admin/appeals", methods=["POST", "GET"])
def admin_appeal_page():
	if request.method == "GET":
		id = users.user_id()
		if id == 0 or not users.check_if_admin(id):
			error_statement = "You shouldn't go there ;)"
			return default_homepage_with_error(error_statement)
		list = ban_appeals.get_list()
		return render_template("adminappeals.html", appeals = list, admin = users.check_if_admin(id))
	if request.method == "POST":
		check_csrf()
		banned_user = request.form.get("banned_user")
		ban_appeals.solve(banned_user)
		users.ban_unban(banned_user)
		return redirect("/admin/appeals")

@app.route("/search", methods=["POST", "GET"])
def search():
	user_id = users.user_id()
	if user_id == 0 and request.method == "GET":
		return render_template("search.html")
	if is_user_banned():
		return redirect("/banned")
	if request.method == "GET":
		return render_template("search.html", admin = users.check_if_admin(user_id))
	if request.method == "POST":
		if user_id != 0:
			check_csrf()
		search_content = request.form.get("search_content")
		if not search_content:
			return redirect("/search")
		search_users = users.search(search_content)
		search_threads = threads.search(search_content)
		search_messages = messages.search(search_content)
		show_results = True
		return render_template("search.html",
		 search_users = search_users, search_threads = search_threads, 
		 search_messages = search_messages, search_content = search_content, 
		 show_results = show_results)

@app.route("/section/<int:id>")
def section(id):
	if not thread_subsections.does_subsection_exist(id) or thread_subsections.is_deleted(id):
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
	list = threads.get_threads_subsection(id)
	title = thread_subsections.get_title(id)
	user_id = users.user_id()
	if user_id == 0:
		return render_template("section.html", list = list, title = title)
	if is_user_banned():
		return redirect("/banned")
	return render_template("section.html", list = list, title = title, id = id)
		
@app.route("/ban", methods = ["POST", "GET"])
def ban():
	user_id = users.user_id()
	if user_id == 0 or not users.check_if_admin(user_id):
		error_statement = "You shouldn't go there ;)"
		default_homepage_with_error(error_statement)
	if request.method == "GET":
		error_statement = "You shouldn't go there ;)"
		default_homepage_with_error(error_statement)
	if request.method == "POST":
		check_csrf()
		ban_unban = request.form.get("user_id")
		users.ban_unban(ban_unban)
		return redirect("/admin/users")

@app.route("/banned", methods = ["POST", "GET"])
def banned():
	user_id = users.user_id()
	if user_id == 0 or not is_user_banned():
		error_statement = "You shouldn't go there ;)"
		default_homepage_with_error(error_statement)
	if request.method == "GET":
		appeal = ban_appeals.check_pending_appeal(user_id)
		return render_template("banned.html", appeal = appeal)
	if request.method == "POST":
		check_csrf()
		appeal_content = request.form.get("appeal_content")
		if len(appeal_content) == 0 or len(appeal_content) > 1000:
			return redirect("/banned")
		ban_appeals.new_appeal(appeal_content, user_id)
		return redirect("/banned")

def is_user_banned():
	user_id = users.user_id()
	if user_id == 0:
		return False
	if not users.check_if_banned(user_id):
		return False
	else:
		return True

def default_homepage_with_error(error_statement):
	list = threads.get_list_of_threads()
	subsections = thread_subsections.get_list_of_subsections()
	id = users.user_id()
	if id == 0:
		return render_template("index.html", list_of_threads = list, error_statement = error_statement, subsections = subsections)
	if is_user_banned():
		return redirect("/banned")
	else:
		user = users.get_username(id)
		admin = users.check_if_admin(id)
		return render_template("index.html", list_of_threads = list, username = user, 
			error_statement = error_statement, admin = admin, subsections = subsections)

def check_csrf():
	if session["csrf_token"] != request.form["csrf_token"]:
		error_statement = "You shouldn't go there ;)"
		return default_homepage_with_error(error_statement)
