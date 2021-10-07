from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def register(username, password, is_admin):
	hash_value = generate_password_hash(password)
	try:
		sql = "INSERT INTO users (username, password, is_admin, banned) VALUES (:username, :password, :is_admin, False)"
		db.session.execute(sql, {"username":username, "password":hash_value, "is_admin":is_admin, "banned":False})
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
	else:
		if check_password_hash(user.password, password):
			session["user_id"] = user.id
			return True
		else:
			return False

def logout():
	del session["user_id"]

def user_id():
	return session.get("user_id",0)

def get_username(id):
	sql = "SELECT username FROM users WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	username = result.fetchone()[0]
	return username

def check_if_admin(id):
	sql = "SELECT is_admin FROM users WHERE id=:id"
	result = db.session.execute(sql, {"id":id})
	admin = result.fetchone()[0]
	if not admin:
		return False 
	else:
		return True 

def get_list_of_users():
	sql = "SELECT id, username, is_admin, banned FROM users" 
	result = db.session.execute(sql)
	return result.fetchall()
	