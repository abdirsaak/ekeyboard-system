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



    

class Products:
    def __init__(self, connection):
        try:
            self.connection = connection
            self.cursor = connection.cursor()
        except Exception as err:
            print('Something went wrong! Internet connection or database connection.')
            print(f'Error: {err}')
    


    def create_product(self,Product_name,Product_price,Product_img_1,Product_img_2,Product_descrpt_1,Product_descrpt_2,category_name,inventory_quantity):
        sql = "INSERT INTO products(Product_name,Product_price,Product_img_1,Product_img_2,Product_descrpt_1,Product_descrpt_2,category_name,inventory_quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            self.cursor.execute(sql, (Product_name,Product_price,Product_img_1,Product_img_2,Product_descrpt_1,Product_descrpt_2,category_name,inventory_quantity,))
            self.connection.commit()
            print("si sax eh aya roo xareeyey product")
            return True, "si sax ayd u xareysay"
        
        except Exception as e:
            print(f"error ayaa jiro, in la xareeyo product: {e}")
            return False, f"error: {e}"
        
    def view_category_name(self,category_name):
        sql = "SELECT category_name FROM products where category_name = %s"
        try:
            self.cursor.execute(sql, (category_name,))
            category_name = self.cursor.fetchall()
            print(f"category_name: {category_name}")
            return category_name
        except Exception as e:
            print(f"error ayaa jiro, in la soo xa: {e}")
            return False, f"error: {e}"
    

    def dispay_product_info(self):
        sql  = "select * from products"
        try:
            self.cursor.execute(sql)
            products = self.cursor.fetchall()

            # print(f"all products info: {products}")

            return products

        except Exception as e:
            print(f"erro while display product: {e}")
            return False, f"error while displaying product info: {e}"
    
    # update_products
    def update_products(self,Product_name,Product_price,Product_img_1,Product_img_2,Product_descrpt_1,Product_descrpt_2,category_name,inventory_quantity,Product_id):
        sql = "UPDATE products SET Product_name = %s,Product_price = %s,Product_img_1 = %s,Product_img_2 = %s,Product_descrpt_1 = %s,Product_descrpt_2 = %s,category_name = %s,inventory_quantity = %s WHERE Product_id = %s"
        try:
            self.cursor.execute(sql, (Product_name,Product_price,Product_img_1,Product_img_2,Product_descrpt_1,Product_descrpt_2,category_name,inventory_quantity,Product_id,))
            self.connection.commit()
            print("si sax eh aya loo update gareeyey product")
            return True, "si sax ayd u xareysay"
        
        except Exception as e:
            print(f"error ayaa jiro, in la update gareeyo product: {e}")
            return False, f"error: {e}"
        

    
    # ...delete product
    def delete_product(self,Product_id):
        sql = "DELETE FROM products WHERE Product_id = %s"
        try:
            self.cursor.execute(sql, (Product_id,))
            self.connection.commit()
            print("si sax eh aya loo tirtiray product")
            return True, "si sax ayd u tirtiray"
        
        except Exception as e:
            print(f"error ayaa jiro, in la tirtiro product: {e}")
            return False, f"error: {e}"
        

    # product cart, storing user_id,product_id,qty
    def product_cart(self,user_id,product_id,qty):
        sql = "INSERT INTO product_carts(user_id,product_id,qty) VALUES (%s,%s,%s)"
        try:
            self.cursor.execute(sql, (user_id,product_id,qty,))
            self.connection.commit()
            print("si sax eh aya loo xareeyey product cart")
            return True, "si sax ayd u xareysay"
        
        except Exception as e:
            print(f"error ayaa jiro, in la xareeyo product cart: {e}")
            return False, f"error: {e}"
        
    # ... get_product_cart by product_id and user_id , not to store dublicate
    def get_product_cart(self,user_id,product_id):
        sql = "SELECT * FROM product_carts WHERE user_id = %s AND product_id = %s"
        try:
            self.cursor.execute(sql, (user_id,product_id,))
            product_cart = self.cursor.fetchall()
            print(f"product_cart: {product_cart}")
            return product_cart
        except Exception as e:
            print(f"error ayaa jiro, in la soo xa: {e}")
            return False, f"error: {e}"






   

   
  
    
  




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
        trainee = Products(mysql_connect.connection)
        return True, trainee
    except Exception as e:
        print(f'creating roduct error database: {e}')
        return False, f'Error: {e}.'
        
        
       

    
   