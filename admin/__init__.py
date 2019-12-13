from flask import Blueprint

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/api/v1/admin')


from admin import admin