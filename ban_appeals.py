from db import db
import users

def get_list():
	sql = "SELECT U.id, U.username, B.content FROM users U, ban_appeals B WHERE (U.id=B.user_id AND B.solved=False)"
	result = db.session.execute(sql)
	return result.fetchall()

def new_appeal(content, user_id):
	if user_id == 0:
		return False
	if len(content) == 0:
		return False
	else:
		sql = "INSERT INTO ban_appeals (user_id, content, solved) VALUES (:user_id, :content, False)"
		db.session.execute(sql, {"user_id":user_id, "content":content})
		db.session.commit()
		return True

def solve(user_id):
	if user_id == 0:
		return False
	else:
		sql = "UPDATE ban_appeals SET solved=True WHERE user_id=:user_id"
		db.session.execute(sql, {"user_id":user_id})
		db.session.commit()
		return True

def check_pending_appeal(user_id):
	if user_id == 0:
		return False
	else:
		sql = "SELECT solved FROM ban_appeals WHERE (user_id=:user_id AND solved=False)"
		result = db.session.execute(sql, {"user_id":user_id})
		if result.rowcount == 0:
			return False
		solved = result.fetchone()[0]
		if solved:
			return False
		return True
