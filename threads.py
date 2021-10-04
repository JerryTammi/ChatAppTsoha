from db import db
import users

def new_thread(title):
	user_id = users.user_id()
	if user_id == 0:
		return False
	else:
		sql = "INSERT INTO message_threads (title, user_id, created, last_updated, deleted) VALUES (:title, :user_id, NOW(), NOW(), False) RETURNING id"
		result = db.session.execute(sql, {"title":title, "user_id":user_id})
		db.session.commit()
		return result.fetchone()[0] 

def get_list_of_threads():
	sql = "SELECT M.id, M.title, M.user_id, M.created, U.username, M.last_updated FROM message_threads M, users U WHERE (M.user_id=U.id AND M.deleted=False) ORDER BY M.created DESC"
	result = db.session.execute(sql)
	return result.fetchall()

def get_thread_details(id):
	sql = "SELECT M.title, M.created, U.username FROM message_threads M, users U WHERE (M.id=:id AND M.user_id=U.id)"
	result = db.session.execute(sql, {"id":id})
	return result.fetchall()

def does_thread_exist(id):
	sql = "SELECT id FROM message_threads WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	if result.rowcount == 0:
		return False
	else:
		return True

