from flask import Blueprint, render_template, request
from API.api import GetAllProducts, GetSingleProducts, GetCategories
products_bp = Blueprint('products_bp', __name__,
    template_folder='templates',
    static_folder='static')

@products_bp.route('/products')
def index():
    data = GetAllProducts()
    l = len(data)
    
    return render_template('products/products.html', length = l, products = data)

@products_bp.route('/products/<int:id>')
def detailOfProduct(id):
    OneProduct = GetSingleProducts(id)

    count = 0
    data = []
    for item in GetAllProducts():
        if(item['category'] == OneProduct['category']):
            count = count + 1
            data.append(item)
        if(count == 4):
            break

    return render_template('products/detail.html', detailOfPorduct = OneProduct, OtherProducts = data)

@products_bp.route('/process-selection', methods=['POST', 'GET'])
def process_selection():
    if request.method == 'POST':
        selected_item = request.form.get('selected_item')
        data = []
        for item in GetAllProducts():
            if(item['category'] == selected_item):
                data.append(item)
        l = len(data)
        categories = GetCategories()

        return render_template('products/sort.html', products = data, length = l, categories = categories)
    
    return render_template('products/products.html', products = GetAllProducts(), length = len(GetAllProducts()), categories = categories)
