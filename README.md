# ChatAppTsoha 2021

[Heroku link](https://chatapptsoha.herokuapp.com/)

## Premade accounts

* Admin user: username = adminuser, pw = password
* Normal user: username = user, pw = password
* Banned user: username = banneduser, pw = password

## Features

* Creating a user. The account can either be a normal or admin one. Obviously in a proper app there wouldn't be the option to create an admin account.
* Logging in and out.
* Creating a new thread and posting messages into existing threads.
* Users can edit their own messages.
* Threads are created within subsections.
* Users can delete their messages and threads.
* Admins can delete all messages and threads.
* Search results will display all users, messages and threads that contain the criteria.
* Admins can ban normal accounts.
* Banned accounts can send a ban appeal that admins can approve.
* Admins can view all users.
* Admins can view all subsections and add new ones or delete existing ones.

## Installation

The app was coded with Python 3.9.2 and PostgreSQL 13

After downloading and unpacking open a command prompt in the installation foldier:

* Create a virtual environment
```
py -m venv virtual
```
```
source virtual/scripts/activate
```

* Install requirements and create the database
```
pip install -r requirements.txt
```
```
psql < schema.sql
```

* Run the app
```
flask run
```
