from app import app
from flask import Flask, json,request, render_template,redirect,session,flash,url_for
from app.DB_configration import MyConfiguration
from app.models.users_db import Database
from app.models.users_db import customers
from flask_bcrypt import Bcrypt

# ..... bycrpt waye
bcrypt  =Bcrypt()


my_configuration = MyConfiguration()
def check_connection():
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
        trainee = customers(mysql_connect.connection)

        return True, trainee
    except Exception as e:
        print(f'')
        return False, f'Error: {e}.'


app.config["SECRET_KEY"] = "abdi@12"


    




@app.route("/E-keyboard/admin/login/Orders")
def Orders():
    if session.get('admin_email'):
        print(f"admin session: {session.get('admin_email')}")
        return render_template("orders/order.html")
    else:
        return redirect(url_for('admin_login'))



   

