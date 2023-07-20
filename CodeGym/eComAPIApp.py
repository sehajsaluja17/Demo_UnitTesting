from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary product data
products = [
    {
        'id': 1,
        'name': 'Mac Book Pro',
        'price': 45.55,
        'description': 'Amazing laptop with awesome security'
    },
    {
        'id': 2,
        'name': 'Ipad',
        'price': 29.99,
        'description': 'Easy to use products awesome and seemless experience'
    },
    {
        'id': 3,
        'name': 'All in One Printer',
        'price': 10.88,
        'description': 'Print, Scan and Xerox using a single machine'
    },
    {
        'id': 4,
        'name': 'TV 43 inch',
        'price': 20.15,
        'description': 'Amazing TV with 4k display'
    },
    # Add more products here as needed
]

# Temporary cart data stored in a Python dictionary for each user
carts = {}

# Routes for handling different API endpoints
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = {
        'id': len(products) + 1,
        'name': data.get('name'),
        'price': data.get('price'),
        'description': data.get('description')
    }
    products.append(new_product)
    return jsonify(new_product), 201

@app.route('/cart', methods=['GET'])
def view_cart():
    user_id = request.args.get('user_id')
    cart = carts.get(user_id, {})

    # Create a list to store cart items with additional details
    cart_items = []
    total_amount = 0

    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            item_total = product['price'] * quantity
            total_amount += item_total
            cart_items.append({
                'product_id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity,
                'item_total': item_total
            })

    return jsonify({
        'cart_items': cart_items,
        'total_amount': total_amount
    })

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Add the product to the user's cart or update the quantity if it's already in the cart
    cart = carts.get(user_id, {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    carts[user_id] = cart

    return jsonify(cart)

@app.route('/cart/delete', methods=['POST'])
def delete_from_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    cart = carts.get(user_id, {})
    if product_id in cart:
        del cart[product_id]
        carts[user_id] = cart
        return jsonify({'message': 'Product removed from cart successfully'}), 200
    else:
        return jsonify({'error': 'Product not found in the cart'}), 404

if __name__ == '__main__':
    app.run(debug=True)