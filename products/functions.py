import json
from uuid import uuid4
import pprint
from flask import Response
from database.functions import read_database, write_database

def create_product():
    print('Creating a product...')
    data = read_database()
    print(data)

    product_id = str(uuid4())
    product_name = input('Input your product name: ')
    product_category = input('Input the product category: ')
    product_price = input('Input the product price: ')


    data['products'][product_id] = {
        "product_name": product_name,
        "product_category": product_category,
        "product_price": product_price
    }
    write_database(data)
    print('Done creating product!')

    
def delete_product():
    data = read_database()
    product_name_to_id = {}
    for product_id, product in data['products'].items():
        product_name_to_id[product['product_name']] = product_id

    print(data)
    input_product_name_to_remove = input(f"Please input the product name you want to remove from: {product_name_to_id}!\n")
    product_id_to_remove = product_name_to_id.get(input_product_name_to_remove)
    if product_id_to_remove in data['products']:
        del data['products'][product_id_to_remove]
    write_database(data)
    print(data)

def list_products():
    data = read_database()
    products = data.get('products')

    if products:
        pprint.pprint(products)
        # print(json.dumps(products, indent=4))
    else:
        print('No products in DB!')

def list_product():
    # alegeti o varianta..
    # v1 faceti in 2 pasi: prima data luati`va toate id`urile si pe urma alegeti un id,
    # v2 alternativ puteti da ca input email-ul


    data = read_database()
    products = data.get('products')

    input_product = input("PLease input the product name you want to display: ")

    for product_id, product in products.items():
        if product['product_name'] == input_product:
            pprint.pprint(product)
            break
    else:
        print(f"No product with name {input_product} has beeen found in DB!")

def update_product():
    data = read_database()
    products = data.get('products')

    input_name = input("PLease input the name of the product you want to update: ")
    updated_name = input("Please input updated name: ")
    updated_category = input("Please input updated category: ")
    updated_price = input("Please input updated price: ")


    for product_id, product in products.items():
        if product['product_name'] == input_name:
            product['product_name'] = updated_name if updated_name else product['product_name']
            product['product_category'] = updated_category if updated_category else product['product_category']
            product['product_price'] = updated_price if updated_price else product['product_price']
            break

    else:
        print(f'No product with the name {input_name} has been found!')

    write_database(data)


## WEB APIs

def create_product_flask(product_name, product_category, product_price):
    data = read_database()
    product_id = str(uuid4())

    data['products'][product_id] = {
        'product_name': product_name,
        'product_category': product_category,
        'product_price': product_price
    }
    write_database(data)

    return 201, product_id


def delete_product_flask(product_id):

    data = read_database()

    if product_id in data.get('products'):
        del data['products'][product_id]
        write_database(data)
        return 200, f"Product with id: {product_id} has been successfully deleted"
        # return Response(status=200, response=f"Product with id: {product_id} has been successfully deleted")

    else:
        return 404, f"Product with id: {product_id} has not been found in DB!"
        # return Response(status=404, response=f"Product with id: {product_id} has not been found in DB!")

def list_products_flask():
    """REST API to list all products from our json db.
    :return: tuple of form (status_code, response_body)
    where response body is a dict of products or a message of error if no users found.
    """
    data = read_database()
    products = data.get('products')

    if products:
        # pprint.pprint(products)
        return 200, products
        # print(json.dumps(products, indent=4))
        # return Response(status=200, response=products)
    else:
        # print('No products in DB!')
        return 404, 'No products in DB!'
        # return Response(status=404, response="No products in DB!")



def get_product_flask(product_id):
    """REST API to retrieve information of a given product from our json db.
    :param product_id_id: uid str, id of the product to be returned
    :return: tuple of form (status_code, response_body)
    """

    data = read_database()
    products = data.get('products')

    if product_id in products:
        # print(f"Product: {json.dumps(products, indent=4)}")
        # return 200, f"Product: {products[product_id]}"
        return Response(status=200, response=f"Product: {products[product_id]}")

    else:
        # return 404, f"No product with id: {product_id} has been found in DB!"
        return Response(status=400, response=f"No product with id: {product_id} has been found in DB!")


def update_product_flask(product_id, product_data):
    """REST API to update product in our json db.
    :param product_id: uid str, id of the product to be updated
    :return: tuple of form (status_code, response_body)
    """

    data = read_database()
    products = data.get('products')

    if product_id in products:
        data['products'][product_id].update(product_data)
        write_database(data)
        return 200, f"Product with id: {product_id} has been successfully updated!"
    else:
        return 404, f"No product with id: {product_id} has benn found in DB!"