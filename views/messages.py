from db import db
import users, threads 

def get_list(thread_id):
	sql = "SELECT M.content, U.username, M.sent_at, M.id, M.user_id, U.is_admin FROM messages M, users U WHERE (M.user_id=U.id AND M.deleted=False AND U.banned=False AND M.message_thread_id=:thread_id) ORDER BY M.sent_at"
	result = db.session.execute(sql, {"thread_id":thread_id})
	return result.fetchall()

def get_sender_id(id):
	sql = "SELECT user_id FROM messages WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	sender_id = result.fetchone()[0]
	return sender_id

def new_message(content, message_thread_id):
	user_id = users.user_id()
	if user_id == 0:
		return False
	if len(content) == 0:
		return False 
	else:
		sql = "INSERT INTO messages (content, user_id, message_thread_id, sent_at, deleted) VALUES (:content, :user_id, :message_thread_id, NOW(), False)"
		db.session.execute(sql, {"content":content, "user_id":user_id, "message_thread_id":message_thread_id})
		db.session.commit()
		threads.update_last_updated(message_thread_id)
		return True 

def delete_message(id):
	user_id = users.user_id()
	if user_id == 0:
		return False
	if users.check_if_admin(user_id) or get_sender_id(id) == user_id:
		sql = "UPDATE messages SET deleted=True WHERE id=:id"
		db.session.execute(sql, {"id":id})
		db.session.commit()
		return True
	return False

def edit_message(id, content):
	user_id = users.user_id()
	if user_id == 0:
		return False
	if len(content) == 0:
		return False
	if get_sender_id(id) == user_id:
		sql = "UPDATE messages SET content=:content WHERE id=:id"
		db.session.execute(sql, {"id":id, "content":content})
		db.session.commit()
		return True
	return False

def search(content):
	sql = "SELECT M.content, T.title, T.id FROM messages M, message_threads T WHERE (content LIKE :content AND T.id=M.message_thread_id AND M.deleted=False AND T.deleted=False)"
	result = db.session.execute(sql, {"content":"%"+content+"%"})
	messages = result.fetchall()
	return messages
	