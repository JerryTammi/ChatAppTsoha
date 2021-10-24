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
	sql = "SELECT id, title, deleted FROM thread_subsections ORDER BY id"
	result = db.session.execute(sql)
	return result.fetchall()

def get_title(id):
	sql = "SELECT title FROM thread_subsections WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	title = result.fetchone()[0]
	return title

def get_thread_count(id):
	sql = "SELECT count(id) FROM message_threads WHERE (thread_subsection_id=:id AND deleted=False)"
	result = db.session.execute(sql, {"id":id})
	count = result.fetchone()[0]
	return count

def get_message_count(id):
	sql = "SELECT count(M.id) FROM messages M, message_threads T "\
	"WHERE (T.thread_subsection_id=:id AND M.message_thread_id=T.id AND T.deleted=False AND M.deleted=False)"
	result = db.session.execute(sql, {"id":id})
	count = result.fetchone()[0]
	return count

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
