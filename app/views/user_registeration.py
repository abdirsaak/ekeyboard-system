from app import app
from flask import Flask, json,request, render_template,redirect,session,flash,url_for
from app.DB_configration import MyConfiguration
from app.models.users_db import Database
from app.models.users_db import customers
from flask_bcrypt import Bcrypt
from app.models.products.products_db import Products

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
        products_instance = Products(mysql_connect.connection)

        return True, trainee,products_instance
    except Exception as e:
        print(f'')
        return False, f'Error: {e}.'


app.config["SECRET_KEY"] = "abdi@12"


@app.route("/E-keyboard/register", methods = ["POST", "GET"])
def user_register():
    if session.get('user_email'):
        return redirect(url_for('home_page'))
    else:
        
    
        connection_status, customers,_ = check_connection()
        print("after requies")
        if request.method == "GET":
            
            if connection_status:
                return render_template("users/register.html")
            else:
                return "Connection failed"
        elif request.method == "POST":
            # Process registration form data here
            firstName = request.form.get("first_name")
            secondName = request.form.get("second_name")
            address = request.form.get("address")
            phone = request.form.get("phone")
            email = request.form.get("email")
            password = request.form.get("password")
            # .... passowrd into hash
            
            password_to = bcrypt.generate_password_hash(password).decode('utf-8')
            if not firstName:
                flash("geli magacaaga koowaad")
                return redirect(url_for("user_register"))
            if not secondName:
                flash("geli magacaaga labaad")
                return redirect(url_for("user_register"))
            if not address:
                flash("geli address-kaaga")
                return redirect(url_for("user_register"))
            if not phone:
                flash("geli numberkaa-ga")
                return redirect(url_for("user_register"))
            if not email:
                flash("geli email-kaaga")
                return redirect(url_for("user_register"))
            if not password:
                flash("geli password-kaaga")
                return redirect(url_for("user_register"))
            print(f"all users info is: name:{firstName}, second: {secondName} \n address: {address}, phone: {phone}, \n  email: {email}, passowrd: {password}")
            check_user_email = customers.find_user_email(email)

            if check_user_email:
                flash("emailkan wuu jiraa")
                return redirect(url_for("user_register"))
            else:

                insert_into_database = customers.register_user(firstName,secondName,email,password_to, phone,address)
                print(f"user inserted is: {insert_into_database}")
                user_id = customers.find_user_id(email)
                session["user_id"] = user_id
                session['user_email'] = email
                # products = products_instance.dispay_product_info()

    
                return redirect(url_for("home_page"))
    
                # return render_template("productHomePage/index.html",products = products)

            # ........ geli database-ka
            # Perform registration logic here



  

    
    
@app.route("/",  methods = ["POST", "GET"])
@app.route("/E-keyboard/login", methods = ["POST", "GET"])
def user_login():
    print(f"userka ku jiro session: {session.get('user_email')}")
    connection_status, customers, _ = check_connection()
    if session.get('user_email'):
        return redirect(url_for('home_page'))
    else:

        if request.method == "GET":
          
            if connection_status:
                return render_template("users/login.html")
            else:
                return "Connection failed"
        elif request.method == "POST":
            # Process registration form data here
            email = request.form.get("email")
            password = request.form.get("password")

            if not email:
                flash("geli emaail-kaaga")
                return redirect(url_for("user_login"))
            if not password:
                flash("geli password-kaaga")
                return redirect(url_for("user_login"))
            user_id = customers.find_user_id(email)
            make_login = customers.login_user(email,password)
            print(f"make login: {make_login}")
            # Perform registration logic here
            if make_login:
                session["user_id"] = user_id
                session['user_email'] = email
                flash("si sax ayad login u sameysay")
                return redirect(url_for("home_page"))
            else:
                flash("email ama password-kaaga waa xad")
                return redirect(url_for("user_login"))
           



@app.route("/E-keyboard/logout")
def user_logout():
    if session.get('user_email'):
        session.pop('user_email')
        return redirect(url_for("user_login"))  

    else:
        return redirect(url_for("user_login"))
    

@app.route("/E-keyboard/homePage", methods=["GET", "POST"])
def home_page():
    if session.get('user_email'):
        message = ""
        connection_status, _, products_instance = check_connection()
        if request.method == "GET":
            # Get products and product carts
            products = products_instance.dispay_product_info()
            user_id = session.get("user_id")
            count_product_carts = products_instance.count_product_carts(user_id)
            product_carts = products_instance.display_product_cart(user_id)

            
            return render_template("productHomePage/index.html", products=products, product_carts=product_carts,count_product_carts = count_product_carts)
        elif request.method == "POST":
            user_id = session.get("user_id")
            product_quantities = request.json
            print(f"product_quantity: {product_quantities}")
            for product_id, quantity in product_quantities.items():
                quantity = int(quantity)
                print(f"product_id: {product_id}, quanity: {quantity}")
                invenotry_quantity = products_instance.display_product_inventory(product_id)
                print(f"value of inventory quantity views: {invenotry_quantity}, quantity: {quantity}")
                
                # if isinstance(inventory_quantity, tuple):
                #     inventory_quantity = inventory_quantity[0]
                
                if invenotry_quantity >= quantity:
                    print("wan ku jiraa")
                    print(f"inventory_quantity views: {invenotry_quantity}")
                    update_product_cart = products_instance.update_product_cart(quantity, user_id, product_id)
                    print(f"updated quantity in product_carts: {update_product_cart}")
                    return redirect(url_for('place_order'))

                else:
                    print("walal ma heyno waxaasi saas u badan")
                    message = "walal ma heyno waxaasi saas u badan"
                    return render_template("productHomePage/index.html", message = message)
            return redirect(url_for('home_page'))
            # return redirect(url_for('place_order'))
    else:
        return redirect(url_for('user_login'))



@app.route("/E-keyboard/place-order", methods=["GET", "POST"])
def place_order():
    if session.get('user_email'):
        connection_status, _, products_instance = check_connection()
        if request.method == "GET":  
            user_id = session.get("user_id")
            product_carts = products_instance.display_product_cart(user_id)
            print(f"all product in place order: {[product_carts]}")
            return render_template("productHomePage/place_order.html",product_carts = product_carts)
           
        elif request.method == "POST":
            # Logic to place the order
            return redirect(url_for('order_confirmation'))
    else:
        return redirect(url_for('user_login'))



    
@app.route('/product/<int:product_id>', methods=["GET", "POST"])
def product_detail(product_id):
    # Check database connection
    connection_status, _, products_instance = check_connection()
    if not connection_status:
        return "Database connection error", 500

    # Initialize product_id
    product = None

    # Handle GET request
    if request.method == "GET":
        # Retrieve product information
        products = products_instance.dispay_product_info()
        product = next((product for product in products if product[0] == product_id), None)

        # If product is not found, return 404 error
        if product is None:
            return "Product not found", 404

    # Handle POST request
    elif request.method == "POST":
        # Retrieve form data
        quantity = request.form.get('quantity')
        user_id = session.get("user_id")
        quantity = int(quantity)

       

        try:
            # Check if product_id is valid before attempting to add to cart
            products = products_instance.dispay_product_info()
            product = next((product for product in products if product[0] == product_id), None)

            # ...chech if the product already in the cart
            product_in_cart = products_instance.get_product_cart(user_id, product_id)
            invenotry_quantity = products_instance.display_product_inventory(product_id)
            if product_in_cart:
                flash('mar hore ayad gelisay cart-ga')
                return render_template('productHomePage/product_description.html', product=product,  product_id=product_id)

            else:

                if product is not None:
                    print(f"value quantity detail")
                    # Attempt to add product to cart
                    if invenotry_quantity >= quantity:
                        pass
                        insert_cart = products_instance.product_cart(user_id, product_id, quantity)
                    else:
                        flash("ma heyno hadigaasi macaamiil")
                        return redirect(url_for("product_detail"))
                    
                    # Check if product was successfully added to cart
                    if insert_cart:
                        flash("si sax ayad u ugu dartay")
                    else:
                        flash('wax baa qaldan macaamiil')
                else:
                    # Product not found, set error message
                    flash("wax product malahan")
        except Exception as e:
            # Handle any exceptions that occur during insertion
            print(f"Error inserting product into cart: {e}")
            success_message = f"Error adding product to cart: {e}"

    # Render template with product information and success message
    return render_template('productHomePage/product_description.html', product=product,  product_id=product_id)


