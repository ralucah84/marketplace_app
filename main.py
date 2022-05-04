from users.functions import *

def print_menu_options():
    print(f"Available options: {list(menu_options.keys())}")

def exit_message():
    print('Have a nice day!')

menu_options = {
    "create_user": create_user,
    "delete_user": delete_user,
    "update_user": update_user,
    "get_user": get_user,
    "list_users": list_users,
    "help": print_menu_options,
    "exit": exit_message
}


def main():
    option = ''
    while option != "exit":
        option = input("Choose an option (type help for menu options, exit to leave): ")
        function_to_call = menu_options.get(option)
        if function_to_call:
            function_to_call()
        else:
            print("You did not input a valid option")
            print_menu_options()


if __name__ == '__main__':
    main()