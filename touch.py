import sys
import bcrypt
import sqlite3
from PySide6.QtWidgets import *
from dashboard import Dashboard
dashboard = None

app = QApplication(sys.argv)

connection = sqlite3.connect("tayoru.db")
cursor = connection.cursor()
cursor.execute("""
      CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
      )
""")
connection.commit()
Window = QWidget()
Window.setWindowTitle("Tayoru:)")
Window.resize(800, 400)
pages = QStackedWidget()
login_page = QWidget()
login_layout = QVBoxLayout()
login_title = QLabel("Welcome to Tayoru :)")
login_layout.addWidget(login_title)
login_message = QLabel("")
login_layout.addWidget(login_message)
layout =QVBoxLayout()

title = QLabel("Tayoru:)")
layout.addWidget(title)
 
####registered_usernames = [] 
def signup_clicked():
    username = signup_username.text().strip()
    password = signup_password.text()
    confirm_password = signup_confirm_password.text()

    if username == "":
        signup_message.setText("Username cannot be empty")
        return

    if password == "":
        signup_message.setText("Password cannot be empty")
        return

    if password != confirm_password:
        signup_message.setText("Passwords do not match")
        return

    cursor.execute(
        "SELECT user FROM users WHERE user = ?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        signup_message.setText("Username already exists")
        return

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    cursor.execute(
        "INSERT INTO users (user, password_hash) VALUES (?, ?)",
        (username, hashed_password.decode())
    )

    connection.commit()

    login_message.setText(
        f"Welcome to Tayoru, {username}! Account created successfully."
    )

    signup_username.clear()
    signup_password.clear()
    signup_confirm_password.clear()

    login_username.setText(username)

    pages.setCurrentWidget(login_page)

def back_to_login():
  pages.setCurrentWidget(login_page)
def logout_user():
    global dashboard

    dashboard.close()
    dashboard = None

    login_username.clear()
    login_password.clear()
    login_message.clear()

    Window.show()
def login_clicked():
    global dashboard

    username = login_username.text().strip()
    password = login_password.text()

    if username == "":
        login_message.setText("Please enter your username")
        return

    if password == "":
        login_message.setText("Please enter your password")
        return

    cursor.execute(
        "SELECT password_hash FROM users WHERE user = ?",
        (username,)
    )

    result = cursor.fetchone()

    if result is None:
        login_message.setText("Invalid username or password")
        return

    stored_hash = result[0]

    if bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    ):
        dashboard = Dashboard(username)
        dashboard.logout_requested.connect(logout_user)
        dashboard.show()

        Window.hide()
        login_message.setText(
            f"Login successful! Welcome back, {username}."
        )
    else:
        login_message.setText("Invalid username or password")

##### login page
login_username = QLineEdit()
login_username.setPlaceholderText("username")
login_layout.addWidget(login_username)
login_password = QLineEdit()
login_password.setPlaceholderText("Password")
login_password.setEchoMode(QLineEdit.Password)
login_layout.addWidget(login_password)
login_button = QPushButton("Login")
login_layout.addWidget(login_button)
signup_page_button = QPushButton("Create New Account")
login_layout.addWidget(signup_page_button)
login_page.setLayout(login_layout)
###### signup page
signup_page = QWidget()
signup_layout = QVBoxLayout()
signup_title = QLabel("Create Your Tayoru Account")
signup_layout.addWidget(signup_title) 
signup_username = QLineEdit()
signup_username.setPlaceholderText("Username")
signup_layout.addWidget(signup_username)
signup_password = QLineEdit()
signup_password.setPlaceholderText("Password")
signup_password.setEchoMode(QLineEdit.Password)
signup_layout.addWidget(signup_password)
signup_confirm_password = QLineEdit()
signup_confirm_password.setPlaceholderText("Confirm Password")
signup_confirm_password.setEchoMode(QLineEdit.Password)
signup_layout.addWidget(signup_confirm_password)
signup_message = QLabel("")
signup_layout.addWidget(signup_message)
signup_button = QPushButton("Create Account")
signup_layout.addWidget(signup_button)
back_button = QPushButton("Back to Login")
signup_layout.addWidget(back_button)
signup_page.setLayout(signup_layout)
##### stack
pages.addWidget(login_page)
pages.addWidget(signup_page)
##### button
login_button.clicked.connect(login_clicked)
signup_button.clicked.connect(signup_clicked)

def open_signup():
    signup_message.clear()
    pages.setCurrentWidget(signup_page)
def logout_user():
    global dashboard

    dashboard.close()
    dashboard = None

    login_username.clear()
    login_password.clear()
    login_message.clear()

    Window.show()
def close_application():
    global dashboard

    if dashboard is not None:
        dashboard.close()

    app.quit()

signup_page_button.clicked.connect(open_signup)
back_button.clicked.connect(back_to_login)
###### Layout
window_layout = QVBoxLayout() 
window_layout.addWidget(pages) 
Window.setLayout(window_layout)
Window.closeEvent = lambda event: close_application()
####Application

Window.show()
sys.exit(app.exec())


