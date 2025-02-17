import json

# File path for products (Lambda-compatible location)
FILE_NAME = "/tmp/product.json"

# Initialize the JSON file
def initialize_file():
    try:
        with open(FILE_NAME, "r") as file:
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(FILE_NAME, "w") as file:
            json.dump([], file)

# Read products from file
def read_products():
    initialize_file()
    with open(FILE_NAME, "r") as file:
        return json.load(file)

# Write products to file
def write_products(products):
    with open(FILE_NAME, "w") as file:
        json.dump(products, file, indent=4)

# Validation functions
def validate_product(product):
    """Validate product fields for adding/updating."""
    if "name" not in product or not isinstance(product["name"], str) or not product["name"].strip():
        return "Product name is required and must be a non-empty string."
    if "price" not in product or not isinstance(product["price"], (int, float)) or product["price"] < 0:
        return "Price is required and must be a non-negative number."
    if "category" not in product or not isinstance(product["category"], str) or not product["category"].strip():
        return "Category is required and must be a non-empty string."
    return None

# Add a product
def add_product(product):
    validation_error = validate_product(product)
    if validation_error:
        return {"status": "error", "message": validation_error}

    products = read_products()
    product["id"] = len(products) + 1  # Assign a unique ID
    products.append(product)
    write_products(products)
    return {"status": "success", "product": product}

# Update a product
def update_product(product_id, updated_data):
    products = read_products()
    for product in products:
        if product["id"] == product_id:
            validation_error = validate_product(updated_data)
            if validation_error:
                return {"status": "error", "message": validation_error}

            product.update(updated_data)
            write_products(products)
            return {"status": "success", "product": product}
    return {"status": "error", "message": f"Product with ID {product_id} does not exist"}

# Delete a product
def delete_product(product_id):
    products = read_products()
    updated_products = [product for product in products if product["id"] != product_id]
    if len(products) == len(updated_products):
        return {"status": "error", "message": f"Product with ID {product_id} does not exist"}
    write_products(updated_products)
    return {"status": "success", "deleted": True}

# List all products
def list_products():
    products = read_products()
    if not products:
        return {"status": "error", "message": "No products found"}
    return {"status": "success", "products": products}

# List products by category
def list_products_by_category(category):
    products = read_products()
    filtered_products = [product for product in products if product.get("category") == category]
    if not filtered_products:
        return {"status": "error", "message": f"No products found in category '{category}'"}
    return {"status": "success", "products": filtered_products}

# Lambda handler function
def lambda_handler(event, context):
    action = event.get("action")
    data = event.get("data")

    if action == "add":
        if not data:
            return {"status": "error", "message": "Product data is required to add a product"}
        return add_product(data)

    elif action == "update":
        if not data or "id" not in data:
            return {"status": "error", "message": "Product ID and data are required for update"}
        return update_product(data["id"], data)

    elif action == "delete":
        if not data or "id" not in data:
            return {"status": "error", "message": "Product ID is required for delete"}
        return delete_product(data["id"])

    elif action == "list":
        return list_products()

    elif action == "list_by_category":
        if not data or "category" not in data:
            return {"status": "error", "message": "Category is required to filter products"}
        return list_products_by_category(data["category"])

    else:
        return {"status": "error", "message": "Invalid action"}
