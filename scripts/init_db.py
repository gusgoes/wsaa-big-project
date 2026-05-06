import sys
import os
import getpass
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from mysql.connector import Error
from config.dbconfig import DB_CONFIG


def init_db():
	db_name = DB_CONFIG["database"]
	db_user = DB_CONFIG["user"]
	db_password = DB_CONFIG["password"]

	if not db_password:
		db_password = getpass.getpass(f"Enter MySQL password for '{db_user}': ")

	server_config = {
		"host": DB_CONFIG["host"],
		"user": db_user,
		"password": db_password,
	}

	effective_db_config = dict(DB_CONFIG)
	effective_db_config["user"] = db_user
	effective_db_config["password"] = db_password

	try:
		server_conn = mysql.connector.connect(**server_config)
		server_cursor = server_conn.cursor()
		server_cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
		server_cursor.close()
		server_conn.close()

		db_conn = mysql.connector.connect(**effective_db_config)
		db_cursor = db_conn.cursor()
		db_cursor.execute(
			"""
			CREATE TABLE IF NOT EXISTS book (
				id INT AUTO_INCREMENT PRIMARY KEY,
				title VARCHAR(255) NOT NULL,
				author VARCHAR(255) NOT NULL,
				price DECIMAL(10, 2) NOT NULL CHECK (price >= 0)
			)
			"""
		)
		db_conn.commit()
		db_cursor.close()
		db_conn.close()

		print("Database and table ready")
	except Error as e:
		print(f"Database initialization failed: {e}")


if __name__ == "__main__":
	init_db()