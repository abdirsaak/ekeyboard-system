# app/__init__.py
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "abdi@12"


from .views import user_registeration
from .views.admin import Admin
from .views.products import manage_product
from .views.orders import orders
from .views.dashboard import dashboard


# .........database

from .models import users_db
from .models.admin import adminLogin_db
from .models.products import  products_db
from .models.products import category_db
from .models.dashboard import dashboard_db

