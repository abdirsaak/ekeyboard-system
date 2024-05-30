from app import app
import mysql.connector

from flask import Flask,json,jsonify
from flask_bcrypt import Bcrypt
from app.DB_configration import MyConfiguration

bcrypt = Bcrypt()
class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def make_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)

    def my_cursor(self):
        return self.cursor






def decryptpass(encrypted_password: str, key: bytes) -> str:
    # Create a Fernet object with the given key
    f = Fernet(key)
    # Decrypt the password
    decrypted_password = f.decrypt(encrypted_password.encode())
    return decrypted_password.decode()



    


class Admin:
    def __init__(self, connection):
        try:
            self.connection = connection
            self.cursor = connection.cursor()
        except Exception as err:
            print('Something went wrong! Internet connection or database connection.')
            print(f'Error: {err}')
   



    def login_admin(self, admin_email,admin_password):
        sql = """

            select admin_name,admin_password from Adminstration where admin_email = %s and admin_password = %s
            """
        try:
            self.cursor.execute(sql, (admin_email,admin_password,))
            my_passowrd = self.cursor.fetchall()

            
            print(f"all my passowrd values: {my_passowrd}")
            if my_passowrd:
               
                print('Login Granted')
                return my_passowrd
              
                
            else:
                # login failed
                print("false here")
                return False
            

        except Exception as e:
            print(f"error loggin admin: {e}")
            return False, f"waa error admin loggin: {e}"
    

    # ....admin name
    def get_admin_name(self,admin_email):
        sql = """
          SELECT admin_name FROM Adminstration WHERE admin_email = %s
            """
        try:
            self.cursor.execute(sql,(admin_email,))
            admin_name = self.cursor.fetchall()
            return admin_name

        except Exception as e:
            print(f"error while geting the admin name: {e}")
            return False

 

   

   
  
    
  




my_configuration = MyConfiguration()
def check_admin_connection():
    try:
        mysql_connect = Database(
            host=my_configuration.DB_HOSTNAME,
            port=3306,
            user=my_configuration.DB_USERNAME,
            password=my_configuration.DB_PASSWORD,
            database=my_configuration.DB_NAME
        )
        # Create an instance of the Store class
        mysql_connect.make_connection()
        trainee = Users(mysql_connect.connection)

        return True, trainee
    except Exception as e:
        print(f'')
        return False, f'Error: {e}.'
        
        
       

    
   