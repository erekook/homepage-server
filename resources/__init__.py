from flask import Blueprint

quote_bp = Blueprint('quote_bp', __name__, url_prefix='/api/v1/quote')
blog_bp = Blueprint('blog_bp', __name__, url_prefix='/api/v1/blog')


from resources import quote, blog