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










class Category:
    def __init__(self, connection):
        try:
            self.connection = connection
            self.cursor = connection.cursor()
        except Exception as err:
            print('Something went wrong! Internet connection or database connection.')
            print(f'Error: {err}')
    
    def create_category(self,category_name):
        sql = "INSERT INTO categories(category_name) VALUES (%s)"

        try:
            self.cursor.execute(sql, (category_name,))
            self.connection.commit()
            print("si sax eh aya roo xareeyey category")
            return True, "si sax ayd u xareysay"
        
        except Exception as e:
            print(f"error ayaa jiro, in la xareeyo category: {e}")
            return False, f"error: {e}"
    
    def get_categoryName(self,category_name):
        sql = """
          SELECT category_name FROM categories WHERE category_name = %s
            """
        try:
            self.cursor.execute(sql,(category_name,))
            category = self.cursor.fetchall()
            
            return category

        except Exception as e:
            print(f"error while geting the category name: {e}")
            return False
        
    def display_categories(self):
        sql = """
          SELECT * FROM categories;
            """
        try:
            self.cursor.execute(sql)
            categories = self.cursor.fetchall()
            
            return categories

        except Exception as e:
            print(f"error while geting the categories: {e}")
            return False
        
    
    def update_category(self,category_id,category_name ):
        sql = "UPDATE categories SET category_name = %s WHERE category_id = %s"

        try:
            pass
            self.cursor.execute(sql, (category_name,category_id,))
            self.connection.commit()
            
            return True

        except Exception as e:
            print(f"error while updating: {e}")
            return False


    # delete_category
    def delete_category(self,category_id):
        sql = "DELETE FROM categories WHERE category_id = %s"

        try:
            self.cursor.execute(sql, (category_id,))
            self.connection.commit()
            
            return True

        except Exception as e:
            print(f"error while deleting: {e}")
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
        categories = Category(mysql_connect.connection)
        return True, categories
    except Exception as e:
        print(f'creating roduct error database: {e}')
        return False, f'Error: {e}.'
        
        
       

    
   