#Get Request Data From A Specified resource
#Post Create Resource 
#Put Update Resource
#DELETE Delete a Resource
from flask import Flask, request, jsonify


app = Flask(__name__)

# Simple in-memory "database" (just a dictionary for simplicity)
products = {}

# Route to add a product
@app.route('/add-product', methods=['POST'])
def add_product():
    data = request.get_json()
    product_id = len(products) + 1  # simple auto-increment ID
    products[product_id] = {
        'name': data['name'],
        'price': data['price'],
        'category': data['category']
    }
    return jsonify({'message': 'Product added successfully'}), 201

# Route to list all products
@app.route('/list-product', methods=['GET'])
def list_product():
    return jsonify(products)

# Route to remove a product by ID
@app.route('/remove-product/<int:id>', methods=['DELETE'])
def remove_product(id):
    if id in products:
        del products[id]  # Remove the product
        return jsonify({'message': 'Product removed successfully'})
    return jsonify({'message': 'Product not found'}), 404

# Route to update a product by ID
@app.route('/update-product/<int:id>', methods=['PUT'])
def update_product(id):
    if id in products:
        data = request.get_json()
        # Update product data
        products[id]['name'] = data.get('name', products[id]['name'])
        products[id]['price'] = data.get('price', products[id]['price'])
        products[id]['category'] = data.get('category', products[id]['category'])
        return jsonify({'message': 'Product updated successfully'})
    return jsonify({'message': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
