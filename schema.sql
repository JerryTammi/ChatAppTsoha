CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE, 
	password TEXT, 
	is_admin BOOLEAN, 
	banned BOOLEAN
);

CREATE TABLE thread_subsections (
	id SERIAL PRIMARY KEY, 
	title TEXT
);

CREATE TABLE message_threads (
	id SERIAL PRIMARY KEY, 
	title TEXT, 
	user_id INTEGER REFERENCES users, 
	thread_subsection_id INTEGER REFERENCES thread_divisions, 
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
	id SERIAL PRIMARY KEY, 
	content TEXT
);

CREATE TABLE ban_appeal (
	id SERIAL PRIMARY KEY, 
	user_id REFERENCES users, 
	content TEXT
);
