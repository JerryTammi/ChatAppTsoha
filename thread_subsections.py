from db import db
import users 

def new_subsection(title):
	user_id = users.user_id()
	if not users.check_if_admin(user_id):
		return False
	else:
		sql = "INSERT INTO thread_subsections (title, deleted) VALUES (:title, False)"
		result = db.session.execute(sql, {"title":title})
		db.session.commit()
		return True 

def get_list_of_subsections():
	sql = "SELECT id, title, deleted FROM thread_subsections"
	result = db.session.execute(sql)
	return result.fetchall()

def get_title(id):
	sql = "SELECT title FROM thread_subsections WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	title = result.fetchone()[0]
	return title

def is_deleted(id):
	sql = "SELECT deleted FROM thread_subsections WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	deleted = result.fetchone()[0]
	return deleted

def delete_subsection(id):
	user_id = users.user_id()
	if user_id == 0:
		return False 
	if users.check_if_admin(user_id):
		sql = "UPDATE thread_subsections SET deleted = True WHERE id=:id"
		db.session.execute(sql, {"id":id})
		db.session.commit()
		return True
	return False

def does_subsection_exist(id):
	sql = "SELECT id FROM thread_subsections WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	if result.rowcount == 0:
		return False
	else:
		return True
