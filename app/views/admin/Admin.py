from app import app
from flask import Flask, json,request, render_template,redirect,session,flash,url_for
from app.DB_configration import MyConfiguration
from app.models.users_db import Database
from app.models.admin.adminLogin_db import Admin
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
        trainee = Admin(mysql_connect.connection)

        return True, trainee
    except Exception as e:
        print(f'')
        return False, f'Error: {e}.'


app.config["SECRET_KEY"] = "abdi@12"



# Routes
@app.route("/E-keyboard/admin/login/main-page")
def main_page():
    try:
        if session.get("admin_email"):
            admin_email = session.get("admin_email")
            connection_status, admin_ = check_connection()  # Define connection_status here
            if connection_status:
                get_admin_name = admin_.get_admin_name(admin_email)
                return render_template("/products/main_page.html", get_admin_name=get_admin_name)
            else:
                print(f"Connection is failed")
        else:
            return redirect(url_for("admin_login"))
    except Exception as e:
        return f"View error in main_page: {e}"

    

@app.route("/E-keyboard/admin/login", methods = ["POST", "GET"])
def admin_login():
    print(f"adminka ku jiro session: {session.get('user_email')}")
    connection_status, Admin = check_connection()
    if session.get('admin_email'):
        return redirect(url_for('product_home_page'))
    else:

        if request.method == "GET":
            if connection_status:
                return render_template("admin/admin_login.html")
            else:
                return "Connection failed"
        elif request.method == "POST":
            # soo qaado emailka iyo passowrdka
            email = request.form.get("email")
            password = request.form.get("password")

            if not email:
                flash("geli emaail-kaaga")
                return redirect(url_for("admin_login"))
            if not password:
                flash("geli password-kaaga")
                return redirect(url_for("admin_login"))
            
            make_login = Admin.login_admin(email,password)
            print(f"make login: {make_login}")
            # fii hadii login info lasoo celiyey uu yahay sax ama qalad
            if make_login:
                session['admin_email'] = email  # keedi admin_emailka session-ka
                return redirect(url_for('main_page'))
                # return redirect(url_for('main_page'))
            else:
                flash("email ama password-kaaga waa xad")
                return redirect(url_for("admin_login"))
           







@app.route("/E-keyboard/admin/logout")
def admin_logout():
    if session.get('admin_email'):
        session.pop('admin_email')
        return redirect(url_for("admin_login"))  

    else:
        return redirect(url_for("admin_login"))
    


# ... admin name

    
