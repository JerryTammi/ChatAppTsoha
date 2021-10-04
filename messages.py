from db import db
import users 

def get_list(thread_id):
	sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE (M.user_id=U.id AND M.deleted=False AND U.banned=False AND M.message_thread_id=:thread_id) ORDER BY M.sent_at"
	result = db.session.execute(sql, {"thread_id":thread_id})
	return result.fetchall()

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
		return True 