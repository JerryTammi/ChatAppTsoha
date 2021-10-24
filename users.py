from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

def register(username, password, is_admin):
	hash_value = generate_password_hash(password)
	try:
		sql = "INSERT INTO users (username, password, is_admin, banned) VALUES (:username, :password, :is_admin, False)"
		db.session.execute(sql, {"username":username, "password":hash_value, "is_admin":is_admin})
		db.session.commit()
	except:
		return False
	return True

def login(username, password):
	sql = "SELECT * FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if not user:
		return False
	if check_password_hash(user.password, password):
		session["user_id"] = user.id
		session["csrf_token"] = secrets.token_hex(16)
		if check_if_admin(user.id):
			session["admin"] = True
		return True
	return False

def logout():
	if check_if_admin(user_id()):
		del session["admin"]
	del session["user_id"]
	del session["csrf_token"]

def user_id():
	return session.get("user_id", 0)

def get_username(id):
	sql = "SELECT username FROM users WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	username = result.fetchone()[0]
	return username

def check_if_admin(id):
	sql = "SELECT is_admin FROM users WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	admin = result.fetchone()[0]
	return admin

def check_if_banned(id):
	sql = "SELECT banned FROM users WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	banned = result.fetchone()[0]
	return banned

def get_list_of_users():
	sql = "SELECT id, username, is_admin, banned FROM users ORDER BY id" 
	result = db.session.execute(sql)
	return result.fetchall()

def search(content):
	sql = "SELECT username FROM users WHERE (username LIKE :content AND banned=False)"
	result = db.session.execute(sql, {"content":"%"+content+"%"})
	usernames = result.fetchall()
	return usernames

def ban_unban(id):
	if check_if_banned(id):
		sql = "UPDATE users SET banned=False WHERE id=:id"
		db.session.execute(sql, {"id":id})
		db.session.commit()
		return True
	else:
		sql = "UPDATE users SET banned=True WHERE id=:id"
		db.session.execute(sql, {"id":id})
		db.session.commit()
		return True
	