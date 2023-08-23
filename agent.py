from bank import SubBank
import random
import json
class CreateAgent(SubBank):
    def __init__(self, data_file):
        super().__init__(data_file)
        self.logged_in_agent = None
         #the above line defines a a class that inherits the class subbank which is also a class with the abstract class bank
        # the constructor method for the CreateUser takes the parameter "data_file" which specifies the data file associated with the bank.
        # the super function calls the constructor of the parent class "subbank" which also passes the "data file as a parameter"
        #logged_in_agent is an attribute set as None and it is used to store the data of a user that is currently logged in
        
    def create_agent_account(self):
        new_agent = {} #initialises an empty dictionary to store details of the new user
        new_agent_details = ["FirstName", "LastName", "Age", "pin", "Email"] # this creates a list that contains what agent needs to enter
        for detail in new_agent_details:
            new_agent[detail] = input(f"Enter {detail}: ")
        new_agent['account_num'] = self.generate_account_number()
        new_agent['balance'] = 0
        self.data["agents"].append(new_agent) # the line adds "new_agent" dictionary to the list created in the user dictionaries stored in the "data" dictionary
        self.write_data() # this line calls the method "write_data" from the parent class to save the updaated data to the data file

        print("Agent account has been successfully created")
    def agent_login(self):
        input_email = input("Enter agent email: ")
        input_pin = input("Enter agent PIN: ")
        for agent_info in self.data["agents"]:
            if agent_info["Email"] == input_email and agent_info["pin"] == input_pin:
                print("Login successful!")
                self.logged_in_agent = agent_info  # Stores logged-in agent's info
                self.logged_in_menu()  # Display menu for logged-in agent
                return
        print("Invalid email or PIN. Login failed.")

    def logged_in_menu(self):
        while True:
            print("\nWelcome to Agent Menu:")
            print("1. Pay to User Account")
            print("2. Reset User PIN")
            print("3. Delete User Account")
            print("4. Reset Agent PIN")
            print("5. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.pay_to_user_acct()
            elif choice == "2":
                self.reset_user_pin()
            elif choice == "3":
                self.delete_user_account()
            elif choice == "4":
                self.reset_agent_pin()
            elif choice == "5":
                print("Logged out.")
                self.logged_in_agent = None  # this line of clears the data of the agent after logging out
                break
            else:
                print("Invalid choice. Please select a valid option.")
    
    def pay_to_user_acct(self):
        user_account_num = int(input("Enter user account number: "))
        amount = float(input("Enter amount to be paid to user: "))

        for user_info in self.data["users"]:
            if user_info["account_num"] == user_account_num:
                user_info["balance"] += amount
                self.write_data()
                print(f"The sum of ${amount} has sucessfully been transferred to {user_info['FirstName']} {user_info['LastName']}")
                return
        print("User account not found.")

    def reset_user_pin(self):
        user_account_num = int(input("Enter user account number: "))
        new_pin = input("Enter new PIN: ")

        for user_info in self.data["users"]:
            if user_info["account_num"] == user_account_num:
                user_info["pin"] = new_pin
                self.write_data()
                print(f"The PIN for the user {user_info['FirstName']} {user_info['LastName']} has been reset to {new_pin}")
                return
        print("User account not found.")

    def delete_user_account(self):
        user_account_num = int(input("Enter user account number to delete: "))
        confirm = input("Are you sure you want to delete this account? (yes/no): ")
        if confirm.lower() == "yes":
            self.data["users"] = [user for user in self.data["users"] if user["account_num"] != user_account_num] 
            self.write_data()
            # the codes in line 88-90 uses a kind of comprehension to create a a new list of dictionaries exclusing the one specified
            # so the code loops through the dictionary and excludes the number the agent wants to delete 
            print("User account has been deleted successfully.")
        else:
            print("Account deletion cancelled.")

    def reset_agent_pin(self):
        agent_account_num = int(input("Enter your agent account number: "))
        agent_pin = input("Enter your agent PIN: ")
        agent = None
        for agent_info in self.data["agents"]:
            if agent_info["account_num"] == agent_account_num and agent_info["pin"] == agent_pin:
                agent = agent_info
                break
        if agent is None:
            print("Agent account number or PIN not found.")
            return
        old_password = input("Enter your old PIN: ")
        correct_email = agent["Email"]
        input_email = input("Input your correct email: ")

        if old_password == agent["pin"] or input_email == correct_email:
            new_pin = input("Enter new PIN: ")
            agent["pin"] = new_pin
            self.write_data()
            print("Agent PIN has been reset succesfully.")
        else:
            print("Authentication failed. PIN reset for Agent has been cancelled.")
        
    def generate_account_number(self):
        return random.randint(1000000000, 9999999999)

    def read_data(self, data_file):
        try:
            with open(data_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": [], "agents": []}

    def write_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
agent_manager = CreateAgent("data.json")
    