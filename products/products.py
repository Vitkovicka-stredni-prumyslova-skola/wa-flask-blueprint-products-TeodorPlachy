from flask import Blueprint, render_template, request
from API.api import GetAllProducts, GetSingleProducts, GetCategories, CreateProduct
products_bp = Blueprint('products_bp', __name__,
    template_folder='templates',
    static_folder='static')

@products_bp.route('/products')
def index():
    data = GetAllProducts()
    l = len(data)
    categories = GetCategories()
    return render_template('products/products.html', length = l, products = data, categories = categories, lenCTG = len(categories))

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
    categories = GetCategories()

    return render_template('products/detail.html', detailOfPorduct = OneProduct, OtherProducts = data, categories = categories, length = len(categories))

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
    
    return render_template('products/products.html', products = GetAllProducts(), length = len(GetAllProducts()), categories = categories, lenCTG = len(categories))


@products_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Získání dat formuláře
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        description = request.form['description']
        image = request.form['image']

        # Vytvoření dat pro nový produkt
        new_product_data = {
            "title": name,
            "category": category,
            "price": price,
            "description": description,
            "image": image
        }

        # Vytvoření nového produktu
        CreateProduct(new_product_data)
        return redirect(url_for('api_bp.index'))  # Přesměrování na domovskou stránku nebo jinou cílovou stránku
    else:
        categories = GetCategories()
        return render_template('add_product.html', categories=categories)
    

@products_bp.route('/add-product', methods=['POST', 'GET'])
def checkout():
    if request.method == 'POST':
        itemName = request.form.get('nazev')
        itemCost = request.form.get('cena')
        itemDesc = request.form.get('popis')
        itemCag = request.form.get('category')
        
        data = {
            'title': itemName,
            'price': itemCost,
            'description': itemDesc,
            'image': 'https://i.pravatar.cc',
            'category': itemCag
        }

        # Here you would insert the product into your database or storage mechanism
        # For simplicity, I'll just print the received data
        print("Received product data:", data)

        # Return a JSON response indicating success
        return jsonify({"message": "Product added successfully"})

    return render_template('products/add-product.html')
