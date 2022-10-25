import json
import pprint
from datetime import datetime
from uuid import uuid4

from flask import Response

import sys
print (sys.path)
from database.functions import read_database, write_database



# user template:
# {
#     "b4da16a1-b23f-42c8-aff0-371539fe1553": {
#         "name": "John Doe",
#         "email": "john_doe@gmail.com",
#         "register_date": "2022-04-13 20:44"
# }


def is_valid_email(email):
        """Returns whether an email address string is valid or not.
        :param email: email address str
        :return: tuple of form (True/False, message) if valid/not valid with message explaining the error
        """
        special_characters = "!#$%^&*()|\\{}[]'\":;/><,`~"
        # cautam toate cazurile in care e invalid, deci False
        # iar la final, daca nu am gasit niciun if care sa returneze, inseamna ca e valid, deci True
        if email.count('@') != 1:
            return False, "Email address should contain exactly one @ symbol!"
        if email.count('.') < 1:
            return False, "Email address should contain at least one . symbol!"
        if email.lower() != email:
            return False, "Email address should contain only lowercase letters!"
        # nu trebuie sa contina unul dintre caracterele speciale: !@#$%^&*()|\{}[]'":;/><,`~
        if any(c in email for c in special_characters):
            return False, f"Email address should not contain any of the following special_characters: {special_characters}"
        return True, ""



def create_user():
    # vrem sa facem:
    # 1.cream register_date in mod dinamic
    # 2.verificare email

    print('Creating a user...')
    data = read_database()
    print(data)

    user_id = str(uuid4())
    name = input('Input your user name: ')
    email = input('Input your user email: ') # ar trebui o verificare ca intr`adevar avem un email valid
    while True:
        validation, message = is_valid_email(email)
        if validation:
            break
        else:

            print(message)
            email = input('Please inputa a valid email address: ')


    # while not validation:
    #     email = input('....')
    #     validation = is_valid_email(email)



    register_date = datetime.now().strftime("%Y-%m-%d %H:%M")



    data['users'][user_id] = {
        "name": name,
        "email": email,
        "register_date": register_date
    }
    write_database(data)
    print('Done creating user!')
    
def delete_user():
    data = read_database()
    user_name_to_id = {}
    for user_id,user in data['users'].items():
        user_name_to_id[user['name']] = user_id
    
    print(data)
    input_name_to_remove = input(f"Please input the name you want to remove from: {user_name_to_id}!\n")        
    id_to_remove = user_name_to_id.get(input_name_to_remove)
    if id_to_remove in data['users']:
        del data['users'][id_to_remove]
    write_database(data)
    print(data)

def list_user():
    # alegeti o varianta..
    # v1 faceti in 2 pasi: prima data luati`va toate id`urile si pe urma alegeti un id, 
    # v2 alternativ puteti da ca input email-ul
    
    # v2 input email
    data = read_database()
    users = data.get('users')

    input_email = input("PLease input email of user you want to display: ")

    for user_id, user in users.items():
        if user['email'] == input_email:
            pprint.pprint(user)
            break
    else:
        print(f"No user with email {input_email} has beeen found in DB!")


def list_users():
    data = read_database()
    users = data.get('users')

    if users:
        pprint.pprint(users)
        # print(json.dumps(users, indent=4))
    else:
        print('No users in DB!')

def update_user():
    # permitem modificarea numelui si emailului prin input() (desi in realitate nu prea modificam email`ul..)
    data = read_database()
    users = data.get('users')

    input_email = input("Please input email of user you want to update: ")
    updated_name = input("Please input updated name: ")
    updated_email = input("Please input updated email: ")


    for user_id, user in users.items():
        if user['email'] == input_email:
            user['name'] = updated_name if updated_name else user['name']
            user['email'] = updated_email if updated_email else user['email']
            break

    else:
        print(f'No user with email {input_email} has been found!')

    write_database(data)



## WEB APIs


def list_users_flask():
    """REST API to list all users from our json db.
    :return: tuple of form (status_code, response_body)
    where response body is a dict of users or a message of error if no users found.
    """
    data = read_database()
    users = data.get('users')

    if users:
        # pprint.pprint(users)
        return 200, users
        # print(json.dumps(users, indent=4))
        # return Response(status=200, response=users)
    else:
        # print('No users in DB!')
        return 404, 'No users in DB!'
        # return Response(status=404, response="No users in DB!")


def get_user_flask(user_id):
    """REST API to retrieve information of a given user from our json db.
    :param user_id: uid str, id of the user to be returned 
    :return: tuple of form (status_code, response_body)
    """
    data = read_database()
    users = data.get('users')

    if user_id in users:
        # print(f"User: {json.dumps(user, indent=4)}")
        # return 200, f"User: {users[user_id]}"
        return Response(status=200, response=f"User: {users[user_id]}")

    else:
        # return 404, f"No user with id: {user_id} has been found in DB!"
        return Response(status=400, response=f"No user with id: {user_id} has been found in DB!")


def create_user_flask(name, email):
    """REST API to create user and save it in our json db.
    :param name: str, name of the User to add
    :param email: str, email of the User to add
    :return: tuple of form (status_code, response_body)
    """
    # creati, adaugati la db userul si returnati 
    validation, validation_msg = is_valid_email(email)  # validarile de genu se fac la nivel de front end (de UI)
    if not validation:
        return 400, f"Validation error: {validation_msg}"  # in caz de fail validare email..
        # return Response(status=400, response="Validation error: "+msg)

    data = read_database()
    user_id = str(uuid4())
    register_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    data['users'][user_id] = {
        "name": name,
        "email": email,
        "register_date": register_date
    }
    write_database(data)
    
    return 201, user_id
    # return Response(status=201, response=user_id)


def update_user_flask(user_id, user_data):
    """REST API to update user in our json db.
    :param user_id: uid str, id of the user to be updated 
    :return: tuple of form (status_code, response_body)
    """
    data = read_database()
    users = data.get('users')

    if user_id in users:
        data['users'][user_id].update(user_data)
        write_database(data)
        return 200, f"User with id: {user_id} has been successfully updated!"
    else:
        return 404, f"No user with id: {user_id} has benn found in DB!"


def delete_user_flask(user_id):
    """REST API to update user in our json db.
    :param user_id: uid str, id of the user to be delete 
    :return: tuple of form (status_code, response_body)
    where status_code in (200, 404) and response body should be an explanatory message 
    """
    data = read_database()
    
    if user_id in data.get('users'):
        del data['users'][user_id]    
        write_database(data)
        return 200, f"User with id: {user_id} has been successfully deleted"
        # return Response(status=200, response=f"User with id: {user_id} has been successfully deleted")

    else:
        return 404, f"User with id: {user_id} has not been found in DB!"
        # return Response(status=404, response=f"User with id: {user_id} has not been found in DB!")
