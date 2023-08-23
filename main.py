from customer import CreateUser
from agent import CreateAgent

def main():
    user_manager = CreateUser("data.json")
    agent_manager = CreateAgent("data.json")

    while True:
        print("\nMain Menu:")
        print("1. Create User Account")
        print("2. Create Agent Account")
        print("3. Login")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_manager.create_user_account()
        elif choice == "2":
            agent_manager.create_agent_account()
        elif choice == "3":
            login_menu(user_manager, agent_manager)
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def login_menu(user_manager, agent_manager):
    while True:
        print("\nLogin Menu:")
        print("1. User Login")
        print("2. Agent Login")
        print("3. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_manager.user_login()
        elif choice == "2":
            agent_manager.agent_login()
        elif choice == "3":
            print("Returning to Main Menu.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()