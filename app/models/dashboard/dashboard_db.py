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










class Dashboard:
    def __init__(self, connection):
        try:
            self.connection = connection
            self.cursor = connection.cursor()
        except Exception as err:
            print('Something went wrong! Internet connection or database connection.')
            print(f'Error: {err}')
    
   
    
    def get_all_users(self):
        sql = """
          SELECT count(*) from users
            """
        try:
            self.cursor.execute(sql)
            all_users = self.cursor.fetchall()
         
            return all_users

        except Exception as e:
            print(f"error while geting the all users: {e}")
            return False
        

    def get_total_keyboard(self):
        sql = """
          SELECT count(*) from products
            """
        try:
            self.cursor.execute(sql)
            all_keyboards = self.cursor.fetchall()
            return all_keyboards

        except Exception as e:
            print(f"error while geting the total keyboards: {e}")
            return False
    def get_all_categories(self):
        sql = """
          SELECT count(*) from categories
            """
        try:
            self.cursor.execute(sql)
            all_categories = self.cursor.fetchall()
            return all_categories

        except Exception as e:
            print(f"error while geting the total keyboards: {e}")
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
        dashboard = Dashboard(mysql_connect.connection)
        return True, dashboard
    except Exception as e:
        print(f'creating roduct error database: {e}')
        return False, f'Error: {e}.'
        
        
       

    
   