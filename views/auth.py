from random import randint
from controllers.ui_helper import ui_helper
from queries.read.queries import QUERIES as RE_QUERIES
from queries.create.queries import QUERIES as CRE_QUERIES
from . import client
from random_address import real_random_address

AUTH_PW = "password"

# method for authenticating the admin user
def admin_login():
        pw = ui_helper.get_str("Please enter admin password:\n")
        is_authenticated = False
        while is_authenticated == False:
                if pw == AUTH_PW:
                        print("Correct, password. You are authenticated.")
                        is_authenticated = True
                else:
                        pw = ui_helper.get_str("Error: Incorrect, password. Please re-enter password:\n")
                        continue

# method for user logging into the database
def user_login(db):
        username = ui_helper.get_str("Please enter your username:\n")
        is_authenticated = False
        while is_authenticated == False:
                if username_exists(username, db) == False:
                        username = ui_helper.get_str("Error: Username does not exist. Please re-enter username:\n")
                        continue
                password = ui_helper.get_str("Please enter your password:\n")
                if password != get_user_password(username, db):
                        print("Error: Incorrect password - please try again, goodbye.")
                        continue
                print(f'''Correct, password. You are authenticated.
                \nWelcome {username}!\n''')
                is_authenticated = True
        user_session = True
        while user_session == True:
                choice = client.present_options()
                if choice == 0:
                        break
                elif choice == 1:
                        # present subscriptions by username
                        client.get_subscriptions(db, username)
                elif choice == 2:
                        # present magazine catalog
                        client.display_mag_catalog(db)
                # elif choice == 3:
                #         # add magazine to subscription by username and mag_id
                # elif choice == 4:
                        # soft delete user account by username
                continue
                
# user login helper methods
def username_exists(username, db):
        return db.get_record(RE_QUERIES["CUST_GET_BY_USERNAME"], tuple([username, ]), "username") != None

def get_user_password(username, db):
        return db.get_record(RE_QUERIES["CUST_GET_BY_USERNAME"], tuple([username, ]), "username")[4]

# method for user to sign up for an account
def user_signup(db):
        is_created = False
        while is_created == False:
                username = ui_helper.get_str("Enter a username:\n")
                if username_exists(username, db):
                        print(f"Error: username - {username} - already exists.")
                        continue
                first_name = ui_helper.get_str("Enter your first name: ")
                last_name = ui_helper.get_str("Enter your last name: ")
                name = last_name + ", " + first_name
                password = ui_helper.get_str("Enter a password: ")
                print(f"Username - {username}, Name - {name}, Password - {password}")
                choice = ui_helper.get_choice([0,1], "Enter 1 to confirm your choices, 0 to restart:")
                if choice == 0:
                        continue
                db.single_insert(CRE_QUERIES["CUST_CREATE_NEW"], tuple([first_name, last_name, username, password]))
                is_created = True
        cust_id = get_cust_id(username, db)
        phone_no = ui_helper.get_phone_no()
        print("For the sake of demonstration: a random state, city, street address, zip code, etc will be chosen...")
        rand_add = real_random_address()
        zip_code = rand_add['postalCode']
        state = rand_add['state']
        city = rand_add['city']
        street_addr = rand_add['address1']
        contact_type = randint(0,1)
        print(f"Random Address generated: {street_addr} {city}, {state} {zip_code}")
        print("Creating profile...")
        db.single_insert(CRE_QUERIES["PRO_CREATE_NEW"], tuple([cust_id, phone_no, zip_code, state, city, street_addr, contact_type]))
        print("Profile sucessfully created.")

# user signup helper methods
def get_cust_id(username, db):
        return db.get_record(RE_QUERIES["CUST_GET_BY_USERNAME"], tuple([username, ]), "username")[0]