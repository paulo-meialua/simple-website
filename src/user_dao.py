import os
import mysql.connector

# from passlib.handlers.sha2_crypt import sha512_crypt as crypto


class UserDAO():

    def __init__(self):      
        self.userdb = mysql.connector.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME')
        ) 

    def authenticate_user(self, username: str, plain_password: str):
        def get_user(username):
            with self.userdb.cursor() as cursor:
                cursor.execute("SELECT * FROM user WHERE username=?", username)
                return cursor.fetchone()

        user = get_user(username)
        if not user:
            return False
        # if not crypto.verify(plain_password, user.hashed_password):
        #     return False
        return user
