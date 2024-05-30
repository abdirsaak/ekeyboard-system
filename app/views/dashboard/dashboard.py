from flask import Flask, request, render_template, redirect, session, flash, url_for
from app import app
from app.DB_configration import MyConfiguration
from app.models.users_db import Database
from app.models.dashboard.dashboard_db import Dashboard

from flask_bcrypt import Bcrypt



def check_connection():
    my_configuration = MyConfiguration()
    try:
        mysql_connect = Database(
            host=my_configuration.DB_HOSTNAME,
            port=3306,
            user=my_configuration.DB_USERNAME,
            password=my_configuration.DB_PASSWORD,
            database=my_configuration.DB_NAME
        )
        mysql_connect.make_connection()
        dashbaord_intance = Dashboard(mysql_connect.connection)
        return True, dashbaord_intance
    except Exception as e:
        print(f'Error: {e}')
        return False
    


@app.route("/E-keyboard/admin/login/Dashboard")
def Admin_dashboard():
    if session.get('admin_email'):
        try:
            check,  dashbaord_intance = check_connection()
            pass
            all_users = dashbaord_intance.get_all_users()
            print(f"all users views: {all_users}")
            all_keyboards = dashbaord_intance.get_total_keyboard()
            print(f"all keyboards in views: {all_keyboards}")
            all_categories = dashbaord_intance.get_all_categories()
            print(f"all categories in views: {all_categories}")
            return render_template("products/index.html",all_users = all_users, all_keyboards = all_keyboards,all_categories = all_categories)

        except Exception as e:
            print(f"error in dashboard views: {e}")
            return False
    else:
        return redirect(url_for('admin_login'))





