from db import db
import users

def new_thread(title, thread_subsection_id):
	user_id = users.user_id()
	if user_id == 0:
		return False
	else:
		sql = "INSERT INTO message_threads (title, user_id, thread_subsection_id, created, last_updated, deleted) VALUES (:title, :user_id, :thread_subsection_id, NOW(), NOW(), False) RETURNING id"
		result = db.session.execute(sql, {"title":title, "user_id":user_id, "thread_subsection_id":thread_subsection_id})
		db.session.commit()
		return result.fetchone()[0] 

def get_list_of_threads():
	sql = "SELECT M.id, M.title, M.user_id, M.created, U.username, M.last_updated, M.thread_subsection_id FROM message_threads M, users U WHERE (M.user_id=U.id AND M.deleted=False) ORDER BY M.created DESC"
	result = db.session.execute(sql)
	return result.fetchall()

def get_thread_details(id):
	sql = "SELECT M.title, M.created, U.username, M.user_id FROM message_threads M, users U WHERE (M.id=:id AND M.user_id=U.id)"
	result = db.session.execute(sql, {"id":id})
	return result.fetchall()

def does_thread_exist(id):
	sql = "SELECT id FROM message_threads WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	if result.rowcount == 0:
		return False
	else:
		return True

def get_sender_id(id):
	sql = "SELECT user_id FROM message_threads WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	sender_id = result.fetchone()[0]
	return sender_id

def delete_thread(id):
	user_id = users.user_id()
	if user_id == 0:
		return False 
	if users.check_if_admin(user_id) or get_sender_id(id) == user_id:
		sql = "UPDATE message_threads SET deleted = True WHERE id=:id"
		db.session.execute(sql, {"id":id})
		db.session.commit()
		return True
	return False

def search(content):
	sql = "SELECT title, id FROM message_threads WHERE (title LIKE :content AND deleted=False)"
	result = db.session.execute(sql, {"content":"%"+content+"%"})
	threads = result.fetchall()
	return threads

def update_last_updated(id):
	sql = "UPDATE message_threads SET last_updated=NOW() WHERE id=:id"
	db.session.execute(sql, {"id":id})
	db.session.commit()
