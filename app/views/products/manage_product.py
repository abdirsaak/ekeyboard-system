from flask import Flask, request, render_template, redirect, session, flash, url_for
from app import app
from app.DB_configration import MyConfiguration
from app.models.users_db import Database
from app.models.products.products_db import Products
from app.models.products.category_db import Category
from flask_bcrypt import Bcrypt

import os
import uuid
from werkzeug.utils import secure_filename

# Configuration
STATIC_FOLDER = os.path.abspath('app/static')
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'product_image')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config["SECRET_KEY"] = "abdi@12"
bcrypt = Bcrypt(app)

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        products_instance = Products(mysql_connect.connection)
        categories = Category(mysql_connect.connection)
        return True, products_instance, categories
    except Exception as e:
        print(f'Error: {e}')
        return False
    







@app.route("/E-keyboard/admin/login/create-category", methods=["GET", "POST"])
def create_category():
    if session.get('admin_email'):
        connection_status, _, categories = check_connection()
        if request.method == "GET":
            get_category = categories.display_categories()
            print(f"all categories: {get_category}")
          
            if connection_status:
                return render_template("products/category.html", get_category = get_category)
            else:
                return "Connection failed"
        elif request.method == "POST":
            print("the resquest is Post")
            category_name = request.form.get('category_name')
            if not category_name:
                flash("soo geli category name.")
                return redirect(url_for("create_category"))

         
            chech_category_name = categories.get_categoryName(category_name)
            print(f"all caetgroy names: {chech_category_name}")
            if not chech_category_name:
                insert_category = categories.create_category(category_name)
                flash("Category created successfully.")
                return redirect(url_for("create_category"))
            else:


                flash("hori ayuu u jiray category name-kan")
                return redirect(url_for("create_category"))   
    
    else:
        return redirect(url_for('admin_login'))
    

@app.route("/E-keyboard/admin/login/update-category", methods=["GET", "POST"])
def update_category():
    if session.get('admin_email'):
        connection_status, _, categories = check_connection()
        if request.method == "GET":
            get_category = categories.display_categories()
            print(f"all categories: {get_category}")
            if connection_status:
                return render_template("products/category.html", get_category = get_category)
            else:
                return "Connection failed"
        elif request.method == "POST":
            category_id = request.form.get('category_id')
            category_name = request.form.get('category_name')
            print(f"click category, category-id:{category_id}, category-name: {category_name}")
            if not category_name:
                flash("Please enter category name")
                return redirect(url_for("create_category"))
            if connection_status:
                update_category = categories.update_category(category_id, category_name)
                print(f"updated catergy success: {update_category}")
                flash("Category updated successfully.")
                return redirect(url_for("create_category"))
            else:
                return "Connection failed"
    else:
        return redirect(url_for('admin_login'))
    


# delete_category
@app.route("/E-keyboard/admin/login/delete-category", methods=["GET", "POST"])
def delete_category():
    if session.get('admin_email'):
        connection_status, _, categories = check_connection()
        if request.method == "GET":
            get_category = categories.display_categories()
            print(f"all categories: {get_category}")
            if connection_status:
                return render_template("products/category.html", get_category = get_category)
            else:
                return "Connection failed"
        elif request.method == "POST":
            category_id = request.form.get('category_id')
            print(f"click category, category-id:{category_id}")
            if connection_status:
                delete_category = categories.delete_category(category_id)
                print(f"deleted category success: {delete_category}")
                flash("Category deleted successfully.")
                return redirect(url_for("create_category"))
            else:
                return "Connection failed"
    else:
        return redirect(url_for('admin_login'))


@app.route("/E-keyboard/admin/login/create-product", methods=["GET", "POST"])
def create_product():
    if session.get('admin_email'):
        connection_status, products_instance, categories= check_connection()
        if request.method == "GET":
            if connection_status:
                display_categro = categories.display_categories()
                print(f"on create product view categories: {display_categro}")
                return render_template("products/createProduct.html",display_categro  =display_categro)
            else:
                return "Connection failed"
        elif request.method == "POST":
            try:
                product_name = request.form.get('product_name')
                product_price = request.form.get('product_price')
                product_image_1 = request.files['product_image_1']
                product_image_2 = request.files['product_image_2']
                product_description_1 = request.form.get('product_description_1')
                product_description_2 = request.form.get('product_description_2')
                category_name = request.form.get('product_category')
                inventory_quantity = request.form.get('product_inventory')
                

                # Input validation
                if not product_name:
                    flash("Please enter the product name")
                    return redirect(url_for("create_product"))
                if not product_price:
                    flash("Please enter the product price")
                    return redirect(url_for("create_product"))
                if not product_image_1 or not product_image_2:
                    flash("Please upload both product images")
                    return redirect(url_for("create_product"))
                if not product_description_1 or not product_description_2:
                    flash("Please enter both product descriptions")
                    return redirect(url_for("create_product"))
                if not category_name:
                    flash("Please enter the product category name")
                    return redirect(url_for("create_product"))
                if not inventory_quantity:
                    flash("Please enter the inventory quantity")
                    return redirect(url_for("create_product"))

                # Handle file upload and save
                if allowed_file(product_image_1.filename) and allowed_file(product_image_2.filename):
                    filename1 = secure_filename(product_image_1.filename)
                    filename2 = secure_filename(product_image_2.filename)
                    extension1 = filename1.rsplit('.', 1)[1].lower()
                    extension2 = filename2.rsplit('.', 1)[1].lower()

                    unique_filename1 = f"{uuid.uuid4().hex}.{extension1}"
                    unique_filename2 = f"{uuid.uuid4().hex}.{extension2}"
                    image_1_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename1)
                    image_2_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename2)

                    product_image_1.save(image_1_path)
                    product_image_2.save(image_2_path)

                    print(f"image 1 name: {unique_filename1}, image name 2: {unique_filename2}")
                    # Only store the filenames in the database
                    if connection_status:
                        view_category_name = products_instance.view_category_name(category_name)
                        if not view_category_name:
                            make_insertion = products_instance.create_product(
                                product_name, product_price, unique_filename1, unique_filename2,
                                product_description_1, product_description_2, category_name, inventory_quantity
                            )
                            print(f"waa la xareeyey produc views: {make_insertion}")
                            if make_insertion:
                                flash("Product created successfully")
                                return redirect(url_for("create_product"))
                            else:
                                flash("Error while creating product")
                                return redirect(url_for("create_product"))
                        else:
                            flash("Category name already exists")
                            return redirect(url_for("create_product"))
            except Exception as e:
                return f"Error while creating product: {e}"
    else:
        return redirect(url_for('admin_login'))

@app.route("/E-keyboard/admin/login/view-products", methods=["GET", "POST"])
def view_products():
    if session.get('admin_email'):
        connection_status, products_instance, _ = check_connection()
        if request.method == "GET":
            if connection_status:
                products = products_instance.dispay_product_info()
                return render_template("products/view_products.html", products=products)
            else:
                return "Connection failed"
        return render_template("products/view_products.html")
    else:
        return redirect(url_for('admin_login'))








@app.route("/E-keyboard/admin/login/update-product", methods=["GET", "POST"])
def update_product():
    if session.get('admin_email'):
        connection_status, products_instance, _ = check_connection()
        if request.method == "GET":
            if connection_status:
                products = products_instance.dispay_product_info()
                return render_template("products/view_products.html", products=products)
            else:
                return "Connection failed"
        elif request.method == "POST":
            product_id = request.form.get('product_id')
            product_name = request.form.get('product_name')
            product_price = request.form.get('product_price')
            product_image_1 = request.files['product_image_1']
            product_image_2 = request.files['product_image_2']
            product_description_1 = request.form.get('product_description_1')
            product_description_2 = request.form.get('product_description_2')
            category_name = request.form.get('product_category')
            inventory_quantity = request.form.get('product_inventory')

            # Input validation
            if not product_name:
                flash("Please enter the product name")
                return redirect(url_for("update_product"))
            if not product_price:
                flash("Please enter the product price")
                return redirect(url_for("update_product"))
            if not product_image_1 or not product_image_2:
                flash("Please upload both product images")
                return redirect(url_for("update_product"))
            if not product_description_1 or not product_description_2:
                flash("Please enter both product descriptions")
                return redirect(url_for("update_product"))
            if not category_name:
                flash("Please enter the product category name")
                return redirect(url_for("update_product"))
            if not inventory_quantity:
                flash("Please enter the inventory quantity")
                return redirect(url_for("update_product"))

            # Handle file upload and save
            if allowed_file(product_image_1.filename) and allowed_file(product_image_2.filename):
                filename1 = secure_filename(product_image_1.filename)
                filename2 = secure_filename(product_image_2.filename)
                extension1 = filename1.rsplit('.', 1)[1].lower()
                extension2 = filename2.rsplit('.', 1)[1].lower()

                unique_filename1 = f"{uuid.uuid4().hex}.{extension1}"
                unique_filename2 = f"{uuid.uuid4().hex}.{extension2}"
                
                image_1_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename1)
                image_2_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename2)

                product_image_1.save(image_1_path)
                product_image_2.save(image_2_path)

                print(f"image 1 name: {unique_filename1}, image name 2: {unique_filename2}")
                # Only store the filenames in the database
                if connection_status:
                    view_category_name = products_instance.view_category_name(category_name)
                    if not view_category_name:
                        make_insertion = products_instance.update_products(
                            product_name, product_price, unique_filename1, unique_filename2,
                            product_description_1, product_description_2, category_name, inventory_quantity,product_id
                        )
                        print(f"waa la xareeyey produc views: {make_insertion}")
                        if make_insertion:
                            flash("Product updated successfully")
                            return redirect(url_for("view_products"))
                        else:
                            flash("Error while creating product")
                            return redirect(url_for("view_products"))
                    else:
                        flash("Category name already exists")
                        return redirect(url_for("view_products"))
      
    else:
        return redirect(url_for('admin_login'))


# .... delete product
@app.route("/E-keyboard/admin/login/delete-product", methods=["GET", "POST"])
def delete_product():
    if session.get('admin_email'):
        connection_status, products_instance, _ = check_connection()
        if request.method == "GET":
            if connection_status:
                products = products_instance.dispay_product_info()
                return render_template("products/view_products.html", products=products)
            else:
                return "Connection failed"
        elif request.method == "POST":
            product_id = request.form.get('product_id')
            if connection_status:
                delete_product = products_instance.delete_product(product_id)
                print(f"deleted product success: {delete_product}")
                flash("Product deleted successfully.")
                return redirect(url_for("view_products"))
            else:
                return "Connection failed"
    else:
        return redirect(url_for('admin_login'))
    



# ...insert into cart
@app.route("/E-keyboard/admin/login/insert-into-cart", methods=["GET", "POST"])
def insert_into_cart():
    if session.get('admin_email'):
        connection_status, products_instance, _ = check_connection()
        if request.method == "GET":
            if connection_status:
                products = products_instance.dispay_product_info()
                return render_template("products/view_products.html", products=products)
            else:
                return "Connection failed"
        elif request.method == "POST":
            product_id = request.form.get('product_id')
            quantity = request.form.get('quantity')
            user_id = session.get("user_id")

            print(f"user_id: {user_id}, product_id: {product_id}, quatoty: {quantity}")
            if connection_status:
                insert_cart = products_instance.product_cart(user_id,product_id,quantity)
                print(f"inserted into cart success: {insert_cart}")
                flash("Product inserted into cart successfully.")
                return redirect(url_for("view_products"))
            else:
                return "Connection failed"
    else:
        return redirect(url_for('admin_login'))

# ... user_cart
# @app.route("/E-keyboard/admin/login/view-user-cart", methods=["GET", "POST"])
# def view_user_cart():
#     if session.get('admin_email'):
#         connection_status, products_instance, _ = check_connection()
#         if request.method == "GET":
#             if connection_status:
#                 user_cart = products_instance.view_user_cart()
#                 return render_template("products/user_cart.html", user_cart=user_cart)
#             else:
#                 return "Connection failed"
#         return render_template("products/user_cart.html")
#     else:
#         return redirect(url_for('admin_login'))



    

@app.route("/E-keyboard/admin/login/profile")
def admin_profile():
    if session.get('admin_email'):
        return render_template("admin/profile.html")
    else:
        return redirect(url_for("admin_login"))
