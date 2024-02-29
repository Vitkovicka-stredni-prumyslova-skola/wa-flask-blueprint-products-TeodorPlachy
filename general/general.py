from flask import Blueprint, render_template
from API.api import GetCategories

general_bp = Blueprint('general_bp', __name__,
    template_folder='templates',
    static_folder='static')

@general_bp.route('/')
def index():
    categories = GetCategories()
    
    return render_template('general/index.html', length = len(categories), categories = categories)
