#Au Yu Xuan     TP075145
#Chen Wei Chien TP076472
#Kong Fu Ken    TP075924
#Lam Yew Fei    TP075921
#Ng Xuan Charl  TP075866
import sys
import csv
import datetime
import pandas as pd

def load_user_data(filename):
    user_data = []
    # If the account file does not exist yet, create it with a header so the
    # first run (Register) works without a manual setup step.
    import os
    if not os.path.exists(filename):
        with open(filename, 'w') as new_file:
            new_file.write(f'{"UserID".ljust(10)} | {"Password".ljust(10)}\n')
            new_file.write(f'{"-" * 10}{"-" * 13}\n')
        return user_data
    with open(filename, 'r') as file:
        next(file)  # Skip the header line
        next(file)  # Skip the dashed line
        for line in file:
            if line.strip():
                user_id, password = line.split('|')
                user_data.append((user_id.strip(), password.strip()))
    return user_data

def save_user_data(filename, user_data):
    # Include header lengths in the calculation
    max_user_id_len = max(len(uid) for uid, _ in user_data + [("UserID", "")])
    max_password_len = max(len(pwd) for _, pwd in user_data + [("", "Password")])

    with open(filename, 'w') as file:
        file.write(f'{"UserID".ljust(max_user_id_len)} | {"Password".ljust(max_password_len)}\n')
        file.write(f'{"-" * max_user_id_len}{"-" * (max_password_len + 3)}\n')  # Only dashes for alignment
        for uid, pwd in user_data:
            file.write(f'{uid.ljust(max_user_id_len)} | {pwd.ljust(max_password_len)}\n')

# Load initial data
filepath = 'user_data.txt'
user_data = load_user_data(filepath)

def login(filename, user_data):
    while True:
        print("1. Login")
        print("2. Change password")
        print("3. Register")
        print("4. Exit")
        choice = int(input("Enter your choice (1-4): "))
        # Check if the user's choice is valid (between 1 and 4)
        if 1 <= choice <= 4:
            # Call the corresponding function based on the user's choice
            if choice == 1:
                login_to_main_page(user_data)
            elif choice == 2:
                user_data = change_password(user_data)
                save_user_data(filename, user_data)
            elif choice == 3:
                user_data = register(user_data)
                save_user_data(filename, user_data)
            elif choice == 4:
                print("Exiting")
                sys.exit()  # This will stop the program entirely
        else:
            print("Please choose a number between 1 and 4.")

def login_to_main_page(user_data):
    attempt_limits = 3
    attempts = 0

    # Prompting userID and password
    while attempts < attempt_limits:
        input_userid = input("Enter user ID: ").strip()
        input_password = input("Enter password: ").strip()

        # If login successfully
        if (input_userid, input_password) in user_data:
            print("Login successful")
            main_menu()
            break

        # If login unsuccessfully
        attempts += 1
        attempts_left = attempt_limits - attempts
        if attempts_left > 0:
            print(f"Incorrect user ID or password. You have {attempts_left} attempts left.")
        else:
            print("Terminated from the system")
            sys.exit() # Exit the program if login fails after maximum attempts
    return False

def change_password(user_data):
    userid = input("Enter user ID: ").strip()
    old_password = input("Enter password: ").strip()

    # Check if the user exists and the old password is correct
    found = False
    for i, (uid, pwd) in enumerate(user_data):
        if uid.strip() == userid and pwd.strip() == old_password:
            new_password = input("Enter new password: ").strip()
            user_data[i] = (userid, new_password)  # Update the user's password
            found = True
            break

    if found:
        print("Password changed successfully.")
    else:
        print("Incorrect user ID or password.")
    return user_data

def register(user_data):
    while True:
        new_userID = input("Enter new user ID: ").strip()
        if any(uid == new_userID for uid, _ in user_data):
            print(f"User '{new_userID}' already exists.")
        else:
            break
    new_password = input("Enter new password: ").strip()
    user_data.append((new_userID, new_password))
    print("New user added successfully.")
    return user_data

def main_menu():
    while True:
        print("\nMain Menu")
        print("Home Screen")
        print("1. Initial Inventory Creation")
        print("2. Inventory System Update")
        print("3. Item Inventory Tracking")
        print("4. Search Distributions")
        print("5. Print Reports")
        print("6. Exit")

        option = input("Enter option: ")
        # User select option
        if option == "1":
            create_initial_inventory()
        elif option == "2":
            system_update()
        elif option == "3":
            item_inventory_tracking()
        elif option == "4":
            search_distribution()
        elif option == "5":
            print_reports()
        # Exit back to login
        elif option == "6":
            print("Exiting")
            sys.exit() # This will stop the program entirely
        else:
            print("Please enter number 1 to 6")

# Create txt
def create_initial_inventory():
    # Define a list of options for the user to choose from
    options = ["PPE", "Hospital", "Supplier", "Distribution", "Return to Main Menu"]
    print("Options:")

    while True:
        # Use enumerate to loop over the options list and print each option with a number
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        # Ask the user to enter their choice
        try:
            choice = int(input("Enter your choice (1-5): "))
            # Check if the user's choice is valid (between 1 and 5)
            if 1 <= choice <= 5:
                # Call the corresponding function based on the user's choice
                if choice == 1:
                    create_ppe_file()
                elif choice == 2:
                    create_hospital_file()
                elif choice == 3:
                    create_supplier_file()
                elif choice == 4:
                    create_distribution_file()
                elif choice == 5:
                    print("Returning to the main menu...")
                    break  # Exit the loop to return to main menu
            else:
                print("Please choose a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def create_ppe_file():
    # Open a file called 'ppe.txt' in write mode
    with open('ppe.txt', 'w') as file:
        # List to hold all the item details
        items = []

        # Ask the user to enter the number of items
        num_items = int(input("Enter the number of items: "))

        # Check if the user entered a valid number (more than 0)
        if num_items < 1:
            print("Please enter a number more than 0")
            return

        # Collect all data first
        for i in range(num_items):
            item_code = input(f"Enter item code for item {i+1}: ")
            item_name = input(f"Enter item name for item {i+1}: ")
            item_stock = "100"  # Assuming item stock is fixed at 100 for simplicity
            supplier_code = input(f"Enter supplier code for item {i+1}: ")
            items.append((item_code, item_name, item_stock, supplier_code))

        # Calculate maximum lengths for each field including the headers
        max_code_len = max(len("Item Code"), max(len(item[0]) for item in items)) + 2
        max_name_len = max(len("Item Name"), max(len(item[1]) for item in items)) + 2
        max_stock_len = max(len("Item Stock"), max(len(item[2]) for item in items)) + 2
        max_supplier_len = max(len("Supplier Code"), max(len(item[3]) for item in items)) + 2

        # Create header and separator based on calculated lengths
        header = f"{'Item Code'.ljust(max_code_len)}|{'Item Name'.ljust(max_name_len)}|{'Item Stock'.ljust(max_stock_len)}|{'Supplier Code'.ljust(max_supplier_len)}"
        separator = f"{'-' * max_code_len}{'-' * max_name_len}{'-' * max_stock_len}{'-' * max_supplier_len}".replace(' ', '-')

        # Write headers and separator
        file.write(header + '\n')
        file.write(separator + '\n')

        # Write the item details using calculated widths
        for item in items:
            item_line = f"{item[0].ljust(max_code_len)}|{item[1].ljust(max_name_len)}|{item[2].ljust(max_stock_len)}|{item[3].ljust(max_supplier_len)}"
            file.write(item_line + '\n')

    # Print a success message and display the contents of ppe.txt
    print("All items have been added to ppe.txt. Displaying the contents:")
    with open('ppe.txt', 'r') as file_read:
        for line in file_read:
            print(line, end='')

    # Prompt the user for the next action
    print("\nChoose an option:")
    print("1. Exit")
    print("2. Download as CSV")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '2':
        convert_to_csv('ppe.txt')

def create_hospital_file():
    # Open a file called 'hospital.txt' in write mode
    with open('hospital.txt', 'w') as file:
        hospitals = []

        # Prompt for number of hospitals to enter
        num_hospital = int(input("Enter the number of hospitals: "))
        if num_hospital < 1:
            print("Please enter a number more than 0")
            return

        # Collect hospital data
        for i in range(num_hospital):
            hospital_code = input(f"Enter hospital code for hospital {i+1}: ")
            hospital_name = input(f"Enter hospital name for hospital {i+1}: ")
            hospitals.append((hospital_code, hospital_name))

        # Determine maximum width for each column
        headers = ["Hospital Code", "Hospital Name"]
        column_widths = [max(len(str(item)) for item in [row[i] for row in hospitals] + [header]) for i, header in enumerate(headers)]

        # Create header line with determined widths
        header_line = "|".join(header.ljust(column_widths[i]) for i, header in enumerate(headers))
        file.write(header_line + '\n')
        file.write('-' * len(header_line) + '\n')

        # Write each hospital's data aligned to the headers
        for hospital in hospitals:
            line = "|".join(str(field).ljust(column_widths[i]) for i, field in enumerate(hospital))
            file.write(line + '\n')

    # Print a success message and display the contents of hospital.txt
    print("All items have been added to hospital.txt. Displaying the contents:")
    with open('hospital.txt', 'r') as file_read:
        for line in file_read:
            print(line, end='')

    # Prompt the user for the next action
    print("\nChoose an option:")
    print("1. Exit")
    print("2. Download as CSV")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '2':
        convert_to_csv('hospital.txt')

def create_supplier_file():
    # Open a file called 'supplier.txt' in write mode
    with open('supplier.txt', 'w') as file:
        # List to hold all the supplier details
        suppliers = []

        # Ask the user to enter the number of suppliers
        num_suppliers = int(input("Enter the number of suppliers: "))

        # Check if the user entered a valid number (more than 0)
        if num_suppliers < 1:
            print("Please enter a number more than 0")
            return

        # Collect all data first
        for i in range(num_suppliers):
            supplier_code = input(f"Enter supplier code for supplier {i+1}: ")
            supplier_name = input(f"Enter supplier name for supplier {i+1}: ")
            item_code = input(f"Enter item code for supplier {i+1}: ")
            quantity = input(f"Enter quantity of {item_code} for supplier {i+1}: ")
            while True:
                supply_date = input(f"Enter supply date (YYYY-MM-DD) for supplier {i + 1}: ")
                try:
                    # Validate and format the date
                    formatted_date = datetime.datetime.strptime(supply_date, '%Y-%m-%d').strftime('%Y-%m-%d')
                    break
                except ValueError:
                    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            suppliers.append((supplier_code, supplier_name, item_code, quantity, formatted_date))

        # Calculate maximum lengths for each field including the headers
        max_code_len = max(len("Supplier Code"), max(len(supplier[0]) for supplier in suppliers)) + 2
        max_name_len = max(len("Supplier Name"), max(len(supplier[1]) for supplier in suppliers)) + 2
        max_item_code_len = max(len("Item Code"), max(len(supplier[2]) for supplier in suppliers)) + 2
        max_quantity_len = max(len("Quantity"), max(len(supplier[3]) for supplier in suppliers)) + 2
        max_date_len = max(len("Supply Date"), max(len(supplier[4]) for supplier in suppliers)) + 2

        # Create header and separator based on calculated lengths
        header = f"{'Supplier Code'.ljust(max_code_len)}|{'Supplier Name'.ljust(max_name_len)}|{'Item Code'.ljust(max_item_code_len)}|{'Quantity'.ljust(max_quantity_len)}|{'Supply Date'.ljust(max_date_len)}"
        separator = f"{'-' * max_code_len}{'-' * max_name_len}{'-' * max_item_code_len}{'-' * max_quantity_len}{'-' * max_date_len}".replace(' ', '-')

        # Write headers and separator
        file.write(header + '\n')
        file.write(separator + '\n')

        # Write the supplier details using calculated widths
        for supplier in suppliers:
            supplier_line = f"{supplier[0].ljust(max_code_len)}|{supplier[1].ljust(max_name_len)}|{supplier[2].ljust(max_item_code_len)}|{supplier[3].ljust(max_quantity_len)}|{supplier[4].ljust(max_date_len)}"
            file.write(supplier_line + '\n')

    # Print a success message and display the contents of supplier.txt
    print("All items have been added to supplier.txt. Displaying the contents:")
    with open('supplier.txt', 'r') as file_read:
        for line in file_read:
            print(line, end='')

    # Prompt the user for the next action
    print("\nChoose an option:")
    print("1. Exit")
    print("2. Download as CSV")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '2':
        convert_to_csv('supplier.txt')

def create_distribution_file():
    # Open a file called 'distribution.txt' in write mode
    with open('distribution.txt', 'w') as file:
        # List to hold all the distribution details
        distributions = []

        # Ask the user to enter the number of distributions
        num_distributions = int(input("Enter the number of distributions: "))

        # Check if the user entered a valid number (more than 0)
        if num_distributions < 1:
            print("Please enter a number more than 0")
            return

        # Collect all data first
        for i in range(num_distributions):
            distribution_code = input(f"Enter distribution code for distribution {i+1}: ")
            item_code = input(f"Enter item code for distribution {i+1}: ")
            hospital_code = input(f"Enter hospital code for distribution {i+1}: ")
            quantity_distribution = input(f"Enter quantity distribution of {item_code} for distribution {i+1}: ")
            while True:
                distribution_date = input(f"Enter distribution date (YYYY-MM-DD) for distribution {i + 1}: ")
                try:
                    # Validate and format the date
                    formatted_date = datetime.datetime.strptime(distribution_date, '%Y-%m-%d').strftime('%Y-%m-%d')
                    break
                except ValueError:
                    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            userid = input(f"Enter user ID for distribution {i+1}: ")
            distributions.append((distribution_code, item_code, hospital_code, quantity_distribution, distribution_date, userid))

        # Calculate maximum lengths for each field including the headers
        max_code_len = max(len("Distribution Code"), max(len(dist[0]) for dist in distributions)) + 2
        max_item_code_len = max(len("Item Code"), max(len(dist[1]) for dist in distributions)) + 2
        max_hospital_code_len = max(len("Hospital Code"), max(len(dist[2]) for dist in distributions)) + 2
        max_quantity_len = max(len("Quantity Distribution"), max(len(dist[3]) for dist in distributions)) + 2
        max_date_len = max(len("Distribution Date"), max(len(dist[4]) for dist in distributions)) + 2
        max_userid_len = max(len("User ID"), max(len(dist[5]) for dist in distributions)) + 2

        # Create header and separator based on calculated lengths
        header = f"{'Distribution Code'.ljust(max_code_len)}|{'Item Code'.ljust(max_item_code_len)}|{'Hospital Code'.ljust(max_hospital_code_len)}|{'Quantity Distribution'.ljust(max_quantity_len)}|{'Distribution Date'.ljust(max_date_len)}|{'User ID'.ljust(max_userid_len)}"
        separator = f"{'-' * max_code_len}{'-' * max_item_code_len}{'-' * max_hospital_code_len}{'-' * max_quantity_len}{'-' * max_date_len}{'-' * max_userid_len}".replace(' ', '-')

        # Write headers and separator
        file.write(header + '\n')
        file.write(separator + '\n')

        # Write the distribution details using calculated widths
        for dist in distributions:
            dist_line = f"{dist[0].ljust(max_code_len)}|{dist[1].ljust(max_item_code_len)}|{dist[2].ljust(max_hospital_code_len)}|{dist[3].ljust(max_quantity_len)}|{dist[4].ljust(max_date_len)}|{dist[5].ljust(max_userid_len)}"
            file.write(dist_line + '\n')

    # Print a success message and display the contents of distribution.txt
    print("All items have been added to distribution.txt. Displaying the contents:")
    with open('distribution.txt', 'r') as file_read:
        for line in file_read:
            print(line, end='')

# Prompt the user for the next action
    print("\nChoose an option:")
    print("1. Exit")
    print("2. Download as CSV")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '2':
        convert_to_csv('distribution.txt')

# Update function
def system_update():

    while True:
        try:
            print("Options:")
            print("1. Update")
            print("2. Distribution")
            print("3. Return to Main Menu")
            choice = int(input("Enter your choice (1, 2 or 3): "))

            if choice in [1, 2, 3]:
                if choice == 1:
                    receive_items()
                elif choice == 2:
                    distribute_items()
                elif choice == 3:
                    print("Returning to the main menu...")
                    break  # Exit the loop to return to the main menu
            else:
                print("Please enter option 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def read_data(filename):
    """ Reads data from a file and returns headers and data separately.
    Returns empty lists if the file is missing or has no rows. """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return [], []
    # Drop blank lines
    lines = [line for line in lines if line.strip()]
    if not lines:
        return [], []
    headers = lines[0].strip().split('|')  # Extract headers from the first line
    # Extract data from the remaining lines, excluding lines with only dashes
    data = [line.strip().split('|') for line in lines[1:] if line.strip() and not all(c == '-' for c in line.strip())]
    headers = [header.strip() for header in headers]  # Clean up headers
    data = [[item.strip() for item in row] for row in data]  # Clean up data
    return headers, data

def calculate_column_widths(headers, data):
    """ Calculates maximum column widths based on headers and actual data. """
    widths = [len(header) for header in headers]  # Initialize widths with header lengths
    for row in data:
        for index, item in enumerate(row):
            widths[index] = max(widths[index], len(item))  # Update widths based on data
    return [width + 3 for width in widths]  # Add padding for aesthetics

def format_record(fields, widths):
    """ Formats each field to match the specified widths, ensuring proper alignment. """
    return '|'.join(field.ljust(width) for field, width in zip(fields, widths))  # Format fields to specified widths

def write_data(filename, headers, data):
    """ Writes data back to the file with correct formatting and alignment. """
    widths = calculate_column_widths(headers, data)  # Calculate column widths
    with open(filename, 'w') as file:
        file.write(format_record(headers, widths) + '\n')  # Write headers
        file.write('-' * (sum(widths) + len(headers) - 1) + '\n')  # Write separator line
        for record in data:
            file.write(format_record(record, widths) + '\n')  # Write data records

def append_data(filename, new_record):
    """ Appends a new record to the file, maintaining formatting. """
    headers, existing_data = read_data(filename)  # Read existing data
    existing_data.append(new_record)  # Add the new record to the existing data
    write_data(filename, headers, existing_data)  # Write updated data back to the file

def receive_items():
    headers, inventory = read_data('ppe.txt')  # Read inventory data
    supplier_headers, suppliers = read_data('supplier.txt')  # Read supplier data

    print("Current Inventory:")
    widths = calculate_column_widths(headers, inventory)  # Calculate column widths for inventory
    print(format_record(headers, widths))  # Print headers
    separator_line = '-' * (sum(widths) + len(headers) - 1)
    print(separator_line)  # Print separator line
    for item in inventory:
        print(format_record(item, widths))  # Print each inventory item

    item_code = input("Enter item code: ").strip()  # Get item code from user
    supplier_code = input("Enter supplier code: ").strip()  # Get supplier code from user
    quantity = int(input(f"Enter quantity of {item_code} for supplier: ").strip())  # Get quantity from user

    while True:
        supply_date = input("Enter supply date (YYYY-MM-DD) for supplier: ").strip()  # Get supply date from user
        try:
            datetime.datetime.strptime(supply_date, '%Y-%m-%d')  # Validate date format
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")  # Error message for invalid date format

    updated = False
    supplier_name = next((s[1] for s in suppliers if s[0] == supplier_code), '')  # Find supplier name by supplier code
    for item in inventory:
        if item[0] == item_code and item[-1] == supplier_code:  # Update quantity if item and supplier match
            item[2] = str(int(item[2]) + quantity)
            updated = True
            break

    if updated:
        write_data('ppe.txt', headers, inventory)  # Write updated inventory data
        new_supplier_entry = [supplier_code, supplier_name, item_code, str(quantity), supply_date]  # Create new supplier entry
        append_data('supplier.txt', new_supplier_entry)  # Append new supplier entry
        print(f"Updated quantity for item {item_code} to {item[2]} and added new entry to supplier.")  # Confirmation message
    else:
        print("No matching item code and supplier code found. Please enter correct item code and supplier code.")  # Error message

    # Prompt the next action from user
    print("1. Exit")
    print("2. Download as CSV")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '2':
        convert_to_csv('ppe.txt')
        convert_to_csv('supplier.txt')


def distribute_items():
    headers, inventory = read_data('ppe.txt')  # Read inventory data
    user_headers, users = read_data('user_data.txt')  # Read user data
    hospital_headers, hospitals = read_data('hospital.txt')  # Read hospital data
    distribution_headers, distributions = read_data('distribution.txt')  # Read distribution data

    print("Current Inventory:")
    widths = calculate_column_widths(headers, inventory)  # Calculate column widths for inventory
    print(format_record(headers, widths))  # Print headers
    separator_line = '-' * (sum(widths) + len(headers) - 1)
    print(separator_line)  # Print separator line
    for item in inventory:
        print(format_record(item, widths))  # Print each inventory item

    user_id = input("Enter User ID: ").strip()  # Get user ID from user
    password = input("Enter Password: ").strip()  # Get password from user
    hospital_code = input("Enter Hospital Code: ").strip()  # Get hospital code from user
    item_code = input("Enter Item Code: ").strip()  # Get item code from user
    quantity = int(input(f"Enter quantity of {item_code}: ").strip())  # Get quantity from user

    while True:
        distribution_date = input("Enter distribution date (YYYY-MM-DD): ").strip()  # Get distribution date from user
        try:
            datetime.datetime.strptime(distribution_date, '%Y-%m-%d')  # Validate date format
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")  # Error message for invalid date format

    # Validate user credentials
    if not any(user[0] == user_id and user[1] == password for user in users):
        print("Invalid user ID or password.")
        return

    # Validate hospital code
    if not any(hospital[0] == hospital_code for hospital in hospitals):
        print("Invalid hospital code.")
        return

    # Validate item code and check stock
    item_row = next((row for row in inventory if row[0] == item_code), None)
    if not item_row:
        print("Invalid item code.")
        return

    current_stock = int(item_row[2])
    if current_stock < quantity:
        print("Not enough stock available.")
        return

    # Update stock
    new_stock = current_stock - quantity
    item_row[2] = str(new_stock)

    # Generate new distribution code
    new_distribution_code = f"D{len(distributions) + 1}"

    # Append new distribution record
    new_distribution = [
        new_distribution_code, item_code, hospital_code,
        str(quantity), distribution_date, user_id
    ]
    distributions.append(new_distribution)

    # Ensure headers are correctly formatted
    distribution_headers = [
        "Distribution Code", "Item Code", "Hospital Code",
        "Quantity Distribution", "Distribution Date", "User ID"
    ]

    # Write updated inventory and distribution data
    write_data('ppe.txt', headers, inventory)
    write_data('distribution.txt', distribution_headers, distributions)

    print(f"Distributed {quantity} of {item_code} to hospital {hospital_code}. Updated stock is {new_stock}.")

    # Prompt the next action from user
    print("1. Exit")
    print("2. Download as CSV")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '2':
        convert_to_csv('ppe.txt')
        convert_to_csv('distribution.txt')

def item_inventory_tracking():
    # Load the inventory data from the specified file
    inventory_list = load_data('ppe.txt')

    if inventory_list is None:
        print("Failed to load inventory data.")
        return

    while True:
        try:
            # Display the menu options
            print("\nInventory Tracking Options:")
            print("1. Total available quantity of all items in ascending order by item code.")
            print("2. Items with stock quantity less than 25 boxes")
            print("3. Item stock")
            print("4. Return to Main Menu")

            # Get the user's choice and handle each option
            choice = int(input("Enter your choice (1 to 4): "))
            if choice in [1, 2, 3, 4]:
                if choice == 1:
                    total_available_quantity(inventory_list)
                elif choice == 2:
                    items_with_stock_less_than_25(inventory_list)
                elif choice == 3:
                    item_stock(inventory_list)
                elif choice == 4:
                    print("Returning to the main menu...")
                    break  # Exit the loop to return to the main menu
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")

def load_data(filename):
    try:
        # Load the inventory data from a text file without skipping rows
        df = pd.read_csv(filename, delimiter='|')

        # Manually set the correct column names
        df.columns = ['Item Code', 'Item Name', 'Item Stock', 'Supplier Code']

        # Remove any rows where 'Item Code' is NaN or contains header delimiters
        df = df[~df['Item Code'].str.contains('---|Item Code', na=False)]

        # Clean up data by stripping any extra spaces
        df.columns = df.columns.str.strip()
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()

        # Ensure 'Item Stock' column exists before proceeding
        if 'Item Stock' not in df.columns:
            raise KeyError("'Item Stock' column is missing in the data.")

        # Convert 'Item Stock' column to integer
        df['Item Stock'] = df['Item Stock'].fillna(0).astype(int)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def total_available_quantity(inventory_list):
    try:
        # Sort the inventory list by item code and display total available quantities
        sorted_inventory = inventory_list.sort_values(by='Item Code')
        print("Total available quantity of all items in ascending order by item code:")
        print(sorted_inventory[['Item Code','Item Name', 'Item Stock', 'Supplier Code']].to_string(index=False))
    except Exception as e:
        print(f"Error in total_available_quantity: {e}")


def items_with_stock_less_than_25(inventory_list):
    try:
        # Filter items with stock quantity less than 25 and display them
        low_stock_items = inventory_list[inventory_list['Item Stock'] < 25]
        if low_stock_items.empty:
            print("No items with stock quantity less than 25 boxes.")
        else:
            print("Items with stock quantity less than 25 boxes:")
            print(low_stock_items[['Item Code','Item Name', 'Item Stock', 'Supplier Code']].to_string(index=False))
    except Exception as e:
        print(f"Error in items_with_stock_less_than_25: {e}")


def item_stock(inventory_list):
    try:
        # Prompt user to enter an item code and display the stock for that item
        item_code = input("Enter the item code to check stock: ").strip().upper()
        item_stock = inventory_list[inventory_list['Item Code'] == item_code]
        if not item_stock.empty:
            print(f"Stock for item code {item_code}:")
            print(item_stock[['Item Code','Item Name', 'Item Stock', 'Supplier Code']].to_string(index=False))
        else:
            print(f"No stock information found for item code {item_code}.")
    except Exception as e:
        print(f"Error in item_stock: {e}")

def search_distribution():
    # Prompt user to enter the item code
    item_code = input("Enter the item code: ")

    # Load the data from the file
    filename = 'distribution.txt'  # Adjust the path as needed
    df = pd.read_csv(filename, delimiter='|')

    # Clean up any leading or trailing spaces in column names and values
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()

    # Filter data for the specific item code
    filtered_df = df[df['Item Code'] == item_code]

    # Process each hospital separately
    hospitals = filtered_df['Hospital Code'].unique()
    for hospital in hospitals:
        hospital_data = filtered_df[filtered_df['Hospital Code'] == hospital]
        print(f"Distributions for Item Code: {item_code} at Hospital: {hospital}")
        for index, row in hospital_data.iterrows():
            print(f"  Date: {row['Distribution Date']} - Quantity: {row['Quantity Distribution']}")

        # Calculate and display the total quantity for each hospital
        total_quantity = hospital_data['Quantity Distribution'].sum()
        print(f"  Total Quantity Distributed to {hospital}: {total_quantity}\n")

def print_reports():
    # Load the data from files
    supplier_filename = 'supplier.txt'
    distribution_filename = 'distribution.txt'

    # Read the data into DataFrames
    suppliers_df = pd.read_csv(supplier_filename, delimiter='|')
    distribution_df = pd.read_csv(distribution_filename, delimiter='|')

    # Clean up data: remove extra spaces in column headers and values
    suppliers_df.columns = suppliers_df.columns.str.strip()
    distribution_df.columns = distribution_df.columns.str.strip()

    # Strip spaces from string columns in both DataFrames
    for col in suppliers_df.select_dtypes(include=['object']).columns:
        suppliers_df[col] = suppliers_df[col].str.strip()
    for col in distribution_df.select_dtypes(include=['object']).columns:
        distribution_df[col] = distribution_df[col].str.strip()

    # Handle missing values:
    # Fill missing values in 'Quantity' with 0 and convert to integer
    suppliers_df['Quantity'] = suppliers_df['Quantity'].fillna(0).astype(int)
    # Fill missing values in 'Quantity Distribution' with 0 and convert to integer
    distribution_df['Quantity Distribution'] = distribution_df['Quantity Distribution'].fillna(0).astype(int)
    # Fill missing values in 'Distribution Date' with an empty string
    distribution_df['Distribution Date'] = distribution_df['Distribution Date'].fillna('')

    while True:
        # Prompt user to select a report type
        report_type = input(
            "Enter the report type (1: Suppliers, 2: Hospitals, 3: Transactions, 4: Return to Main Menu): ")

        if report_type == '1':
            # List of suppliers with their PPE equipments supplied
            supplier_code = input("Enter supplier code: ")
            filtered_suppliers = suppliers_df[suppliers_df['Supplier Code'] == supplier_code]
            if not filtered_suppliers.empty:
                # Display supplier information
                print(f"Supplier {supplier_code} has supplied the following PPE equipments:")
                print(filtered_suppliers[['Supplier Name', 'Item Code', 'Quantity', 'Supply Date']])
            else:
                print(f"No data found for supplier code {supplier_code}")

        elif report_type == '2':
            # List of hospitals with quantity of distributed items
            hospital_code = input("Enter hospital code: ")
            filtered_hospitals = distribution_df[distribution_df['Hospital Code'] == hospital_code]
            if not filtered_hospitals.empty:
                # Display hospital distribution details including Distribution Code
                print(f"Hospital {hospital_code} distribution details:")
                print(filtered_hospitals[
                          ['Distribution Code', 'Item Code', 'Quantity Distribution', 'Distribution Date']])
            else:
                print(f"No distribution data found for hospital code {hospital_code}")

        elif report_type == '3':
            # Overall transaction report for a selected month
            year = input("Enter year (YYYY): ")
            month = input("Enter month (MM): ")
            selected_date = f"{year}-{month}"
            # Filter transactions by selected year and month
            filtered_transactions = distribution_df[distribution_df['Distribution Date'].str.startswith(selected_date)]
            if not filtered_transactions.empty:
                # Display transaction details
                print(f"Transactions for {selected_date} are as follows:")
                print(
                    filtered_transactions[['Hospital Code', 'Item Code', 'Quantity Distribution', 'Distribution Date']])
            else:
                print(f"No transactions found for {selected_date}")

        elif report_type == '4':
            # Exit the loop to return to the main menu
            print("Returning to Main Menu...")
            break

        else:
            # Handle invalid input
            print("Invalid input. Please enter a number between 1 and 4.")


def convert_to_csv(txt_files, delimiter='|'):
    # Converts one or multiple text files to CSV format.
    if isinstance(txt_files, str):
        txt_files = [txt_files]  # Convert to list if a single file is provided

    for txt_file in txt_files:
        # Generate the CSV file name by replacing the .txt extension with .csv
        csv_file = txt_file.replace('.txt', '.csv')

        # Open the input text file for reading and the output CSV file for writing
        with open(txt_file, 'r') as infile, open(csv_file, 'w', newline='') as outfile:
            # Create a reader to process the input file using the specified delimiter
            reader = csv.reader(infile, delimiter=delimiter)
            # Create a writer to write to the CSV file, using comma as the delimiter
            writer = csv.writer(outfile)
            # Iterate over all rows in the input file and write them to the output CSV file
            for row in reader:
                writer.writerow(row)

        # Print a success message indicating the creation of the CSV file and its name
        print(f"CSV file {csv_file} created successfully. You can now download the CSV file.")

# Run the login function
login(filepath, user_data)
if __name__ == "__main__":
    main_menu()


