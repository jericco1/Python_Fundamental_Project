from bank import SubBank
import random
import json

class CreateUser(SubBank):
    def _init_(self, data_file):
        super().__init__(data_file)
        self.logged_in_user = None
         #the above line defines a a class that inherits the class subbank which is also a class with the abstract class bank
        # the constructor method for the CreateUser takes the parameter "data_file" which specifies the data file associated with the bank.
        # the super function calls the constructor of the parent class "subbank" which also passes the "data file as a parameter"
        #logged_in_user is an attribute set as None and it is used to store the data of a user that is currently logged in

    def create_user_account(self): 
        new_user = {} #initialises an empty dictionary to store details of the new user
        newusers_one = ["FirstName", "LastName", "Age", "pin", "Email"] # this creates a list that contains what user needs to enter

        for detail in newusers_one:
            new_user[detail] = input(f"Enter {detail}: ") 
        new_user['account_num'] = self.generate_account_number()
        new_user['balance'] = 0
        self.data["users"].append(new_user) # the line adds "new_user" dictionary to the list created in the user dictionaries stored in the "data" dictionary
        self.write_data() # this line calls the method "write_data" from the parent class to save the updaated data to the data file
        print("Your account has successfully been created")
      
    def user_login(self):
        input_email = input("Enter user email: ")
        input_pin = input("Enter user PIN: ")
        for user_info in self.data["users"]:
            if user_info["Email"] == input_email and user_info["pin"] == input_pin:
                print("Login successful!")
                self.logged_in_user = user_info  # at this point the logged in user is updated and stored here
                self.logged_in_menu()  # Display menu for logged-in user
                return
        print("Invalid email or PIN. Login failed.")

    def logged_in_menu(self):
        while True:
            print("\nWelcome to Your Account Menu! Please Proceed:")
            print("1. Display Account Information")
            print("2. Transfer Funds")
            print("3. Reset Pin")
            print("4. Logout")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.display_account_info()
            elif choice == "2":
                self.transfer_funds()
            elif choice == "3":
                self.reset_password()
            elif choice == "4":
                print("Logged out.")
                self.logged_in_user = None  # this line of clears the data of the user after logging out
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def display_account_info(self):
        if self.logged_in_user: # this line checks if there is a currently logged in user
            user_info = self.logged_in_user #the line assigns the dictionary of the logged in user to the variable _user_info
            print("Account Information:")
            print(f"First Name: {user_info['FirstName']}")
            print(f"Last Name: {user_info['LastName']}")
            print(f"Age: {user_info['Age']}")
            print(f"Email Address: {user_info['Email']}")
            print(f"Account Number: {user_info['account_num']}")
            print(f"Balance: {user_info['balance']}")
        else:
            print("You are not logged in. Please log in to view account information.")
   
    def transfer_funds(self):
        sender_account_num = int(input("Input sender's account number: "))
        recipient_account_num = int(input("Input recipient's account number: "))
        sender_pin = input("Input sender's account PIN: ")
        amount = float(input("Input amount to transfer: "))

        sender_found = False # the lines initializes two boolean variables to track if the sender and the receiver accounts have been found respectively
        recipient_found = False # the lines initializes two boolean variables to track if the sender and the receiver accounts have been found  respectively
        for user_info in self.data["users"]: 
            if user_info['account_num'] == sender_account_num and user_info['pin'] == sender_pin:
                sender_found = True # returns true to indicate that sender account is valid
                if user_info['balance'] >= amount: # checks if the sender account is enough for the transaction
                    user_info['balance'] -= amount 
                    for recipient_info in self.data["users"]:
                        if recipient_info['account_num'] == recipient_account_num:
                            recipient_found = True # returns true to indicate that receiver's account is valid
                            recipient_info['balance'] += amount
                            print(f"The sum of ${amount} been deducted from {user_info['FirstName']} {user_info['LastName']} and transferred to {recipient_info['FirstName']} {recipient_info['LastName']}")
                            self.write_data() # calls this method to provide an update to the file
                            return
        if not sender_found:  #this line checks if the sender account is not valid or found
            print("Invalid sender account number or PIN.")
        elif not recipient_found: #this line checks if the receiver account is not valid or found
            print("Invalid recipient account number.")
    
    def reset_password(self):
        user_account_num = int(input("Enter user account number: "))
        old_password = input("Enter old PIN: ")
        correct_email = None # the line stores the correct email associated with the provided account after initalizing 
        for user_info in self.data["users"]:
            if user_info["account_num"] == user_account_num:
                correct_email = user_info["Email"] # the line executes when the details match, thus assigns user email to correct_email
                break # this line exits the loop when the correct user is found
        if not correct_email: # line executes when the correct email is not found
            print("Sorry! This user account cannot be found.")
            return # exits the method
        input_email = input("Input your correct email: ")
        if old_password == user_info["pin"] and input_email == correct_email:
            new_password = input("Enter new PIN: ")
            user_info["pin"] = new_password
            self.write_data()
            print("PIN reset has been completed successfully.")
        else:
            print("Authentication failed. Pin reset has been cancelled.")
            
    # Abstract methods from SubBank class
    def generate_account_number(self):
        return random.randint(1000000000, 9999999999)

    def read_data(self, data_file):
        try: # to handle exceptions while reading data from the JSON file
            with open(data_file, 'r') as file:
                return json.load(file) # json.load function is to load the function from the JSon file.. the loaded data which is a dict. is returned by the method
        except (FileNotFoundError, json.JSONDecodeError): # the first error in the exception is raised if the file does not exist, 
            #the second error occurs when there is an issue decoding the JSON data in the file
            return {"users": [], "agents": []} # if there is an exception, an empty agent and user list is returned as default dictionary

    def write_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4) #self.data is the dictionary containing the data to be written in the JSOn data thus representing user data
            # file is the object and represents the file where the JSOn data is to be written to
            # the ensure_ascii simply means that non_ascii characters are written as they are. which means both characters are maintained in their original form
            # the indent_4 here means that there is a proper indentation of four lines from left to right to make the file more readable
user_manager = CreateUser("data.json")