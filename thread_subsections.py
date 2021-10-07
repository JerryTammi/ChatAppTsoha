from db import db
import users 

def new_subsection(title):
	user_id = users.user_id()
	if not users.check_if_admin(user_id):
		return False
	else:
		sql = "INSERT INTO thread_subsections (title) VALUES (:title)"
		result = db.session.execute(sql, {"title":title})
		db.session.commit()
		return True 

def get_list_of_subsections():
	sql = "SELECT id, title FROM thread_subsections"
	result = db.session.execute(sql)
	return result.fetchall()