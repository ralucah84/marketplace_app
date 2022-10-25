from uuid import uuid4
import pprint
from flask import Response
from database.functions import read_database, write_database
from datetime import datetime

def create_order():
    print('Creating an order...')
    data = read_database()
    order_id = str(uuid4())

    userid = None
    user_email = input('Input your e-mail: ')
    for user_id, user in data['users'].items():
        if user['email'] == user_email:
            userid = user_id
            break

    productid = None
    product_to_order = ('Input the product you want to order: ')
    for product_id, product in data['products'].items():
        if product['product_name'] == product_to_order:
            productid = product_id
            break


    if userid is not None and productid is not None:
        register_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        data['orders'][order_id] = {
            "user_id": userid,
            "product_id": productid,
            "register_date": register_date
        }
        write_database(data)
        print('Done creating order')
    else:
        print('Invalid user or product')
    
def delete_order():
    pass

def list_orders():
    pass

def list_order():
    # alegeti o varianta..
    # v1 faceti in 2 pasi: prima data luati`va toate id`urile si pe urma alegeti un id, 
    # v2 alternativ puteti da ca input email-ul
    pass

def update_order():
    pass

def create_order_flask(email, product_name):
    data = read_database()
    orders = data.get(orders)
    order_id = str(uuid4())
    register_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    user_id, product_id = None, None

    for user_id, user in data['users'].items():
        if user[email] == user_email:
            userid = user_id
            break

    for product_id, product in data['products'].items:
        if product[product_name] == product_to_order:
            productid = product_id
            break
        else:
            print('The product does not exist')

    if userid is not None and productid is not None:
        data['orders'][order_id] = {
            "user_id": userid,
            "product_id": productid,
            "register_date": register_date
        }
        write_database(data)
        return 201, f'Order with id {order_id} has been created'
    else:
        return 400, f'Invalid user or product'