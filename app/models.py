"""Learnt from https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way
and
https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""
import json
from flask import jsonify
from datetime import datetime
from passlib.hash import sha256_crypt

from app import DB_conns

db = DB_conns()


class Users:
    """Create Users"""

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = sha256_crypt.encrypt(str(password))

    def signup_user(self):
        db.query(
            "INSERT INTO users(email, username, password) VALUES(%s, %s, %s, %s)",
            (self.email, self.username, self.password))


