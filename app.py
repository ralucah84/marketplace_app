import json

from flask import Flask, request, Response
from users.functions import create_user_flask, delete_user_flask, update_user_flask, list_users_flask, get_user_flask
from products.functions import create_product_flask, delete_product_flask, list_products_flask, get_product_flask, update_product_flask
app = Flask("Marketplace API")

@app.route('/', methods=["GET"])
def hello_world():
    return f"Welcome to the root page of our marketplace API"


@app.route("/list_users", methods=["GET"])
def list_users():
    list_users = list_users_flask()
    return Response(status=list_users[0], response=json.dumps(list_users[1]))



# TODO: implement the missing APIs for users, products and orders

@app.route('/get_user/<user_id>', methods=["GET"])
def get_user(user_id):
    return get_user_flask(user_id)  # return Response object inside functions module...same thing 


@app.route('/add_user', methods=['POST'])
def add_user():
    post_data = json.loads(request.data)
    status_code, new_user_id = create_user_flask(post_data['name'], post_data['email'])  
    # observatii numele cheilor din post_data sunt hardcodate, pentru asta in programare exista conceptul
    # de model de date si ORM-uri, despre care o sa invatam azi
    return Response(status=status_code, response=new_user_id)


@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    status_code, message = delete_user_flask(user_id)
    return Response(status=status_code, response=message)


@app.route('/update_user/<user_id>', methods=['PATCH'])
def update_user(user_id):
    user_data = json.loads(request.data)
    status_code, message = update_user_flask(user_id, user_data)
    return Response(status=status_code, response=message)



@app.route('/add_product', methods=['POST'])
def add_product():
    post_data = json.loads(request.data)
    status_code, new_product_id = create_product_flask(post_data['product_name'], post_data['product_category'], post_data['product_price'])
    return Response(status=status_code, response=new_product_id)


@app.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    status_code, message = delete_product_flask(product_id)
    return Response(status=status_code, response=message)


@app.route("/list_products", methods=["GET"])
def list_products():
    list_products = list_products_flask()
    return Response(status=list_products[0], response=json.dumps(list_products[1]))

@app.route('/get_product/<product_id>', methods=["GET"])
def get_product(product_id):
    return get_product_flask(product_id)  # return Response object inside functions module...same thing



@app.route('/update_product/<product_id>', methods=['PATCH'])
def update_product(product_id):
    product_data = json.loads(request.data)
    status_code, message = update_product_flask(product_id, product_data)
    return Response(status=status_code, response=message)

@app.route('/add_order', methods=['POST'])
def add_order():
    post_data = json.loads(request.data)
    status_code, new_order_id = create_order_flask(post_data['order_id'], post_data['userid'], post_data['productid'])
    return Response(status=status_code, response=new_order_id)

if __name__ == '__main__':
    app.run()
