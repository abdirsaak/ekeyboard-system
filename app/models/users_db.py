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



    


class customers:
    def __init__(self, connection):
        try:
            self.connection = connection
            self.cursor = connection.cursor()
        except Exception as err:
            print('Something went wrong! Internet connection or database connection.')
            print(f'Error: {err}')
   
    def register_user(self, f_name, s_name,user_email,user_password,user_phone,user_address):
        sql = """
                INSERT INTO Users (f_name,s_name, user_email,user_password,user_phone,user_address) VALUES (%s,%s, %s,%s, %s,%s)
                """
        try:
            self.cursor.execute(sql, (f_name,s_name, user_email,user_password,user_phone,user_address))
            self.connection.commit()
            print('si saxan ayad isu diiwan galisay')
            return True, f'si saxan ayad isu diiwan galisay'

        except Exception as e:
            print('mala diiwan galin , cilad aya jirta')
            print(f'Error: {e}')
            return False, f'Error: {e}.'
    
    # find_user_email
    def find_user_email(self, user_email):
        sql = """
            SELECT user_email FROM Users WHERE user_email = %s
        """
        try:
            self.cursor.execute(sql, (user_email,))
            email = self.cursor.fetchall()
            if email:
                return True
            else:
                return False
        except Exception as e:
            print(f'Error: {e}')
            return False
        

    


    def login_user(self, user_email,user_password):
        sql = """

            select f_name,user_password from Users where user_email = %s
            """
        try:
            self.cursor.execute(sql, (user_email,))
            my_passowrd = self.cursor.fetchall()
            if my_passowrd:
                hashed_passowrd = my_passowrd[0][1]
                print('Encripted pass 1: ', type(hashed_passowrd))
                print(f"password hashed databse: {hashed_passowrd}")
                print(f"password plaintext: {hashed_passowrd}")
                compare  = bcrypt.check_password_hash(hashed_passowrd,user_password )
            
                
                print(f"passowrd decripted: {compare}")
                
                # Comprae the two passwords
                if compare:
                    print('Login Granted')
                    return my_passowrd
                else:
                    print('Bad password')
                    return False
                
            else:
                # login failed
                print("false here")
                return False
            

        except Exception as e:
            print(f"error loggin user: {e}")
            return False, f"waa error userka loggin: {e}"
    

    # find userid for the given email
    def find_user_id(self, user_email):
        sql = """
            SELECT user_id FROM Users WHERE user_email = %s
        """
        try:
            self.cursor.execute(sql, (user_email,))
            user_id = self.cursor.fetchall()
            if user_id:
                return user_id[0][0]
            else:
                return False
        except Exception as e:
            print(f'Error: {e}')
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
        
        
       

    
   