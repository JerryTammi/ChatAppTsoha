CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE, 
	password TEXT, 
	is_admin BOOLEAN, 
	banned BOOLEAN
);

CREATE TABLE message_threads (
	id SERIAL PRIMARY KEY, 
	title TEXT, 
	user_id INTEGER REFERENCES users, 
	created TIMESTAMP, 
	last_updated TIMESTAMP, 
	deleted BOOLEAN
);

CREATE TABLE messages (
	id SERIAL PRIMARY KEY, 
	content TEXT, 
	user_id INTEGER REFERENCES users, 
	message_thread_id INTEGER REFERENCES message_threads, 
	sent_at TIMESTAMP, 
	deleted BOOLEAN
);

CREATE TABLE banned_words (

);
