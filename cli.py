from bll import (
    register_user, login_user, logout_user, record_expense, update_expense,
    delete_expense, add_inventory_item, update_inventory, delete_inventory,
    record_sale, update_sale, delete_sale, get_expense_report_by_username,
    get_sales_report_by_username, get_inventory_report, check_authentication
)
from datetime import datetime

authenticated_user = None

def main_menu():
    global authenticated_user
    while True:
        print("\nExpense Tracker CLI")
        print("1. Register User")
        print("2. Login")
        print("3. Expense Management")
        print("4. Inventory Management")
        print("5. Sales Management")
        print("6. Reports")
        print("7. Logout")
        print("8. Exit")

        choice = input("Select an option (1-8): ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            register_user(username, password, email)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if login_user(username, password):
                authenticated_user = username
        elif choice == '3':
            if authenticated_user:
                expense_management()
            else:
                print("Please log in to manage expenses.")
        elif choice == '4':
            if authenticated_user:
                inventory_management()
            else:
                print("Please log in to manage inventory.")
        elif choice == '5':
            if authenticated_user:
                sales_management()
            else:
                print("Please log in to manage sales.")
        elif choice == '6':
            if authenticated_user:
                reports_menu()
            else:
                print("Please log in to view reports.")
        elif choice == '7':
            logout_user()
            authenticated_user = None
        elif choice == '8':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

def expense_management():
    while True:
        print("\nExpense Management")
        print("1. Record Expense")
        print("2. Update Expense")
        print("3. Delete Expense")
        print("4. Back to Main Menu")

        choice = input("Select an option (1-4): ")

        if choice == '1':
            date_str = input("Enter date (YYYY-MM-DD): ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description (optional): ")
            record_expense(authenticated_user, date, amount, category, description)
        elif choice == '2':
            print("\nYour Expenses:")
            expenses = get_expense_report_by_username(authenticated_user)
            for expense in expenses:
                print(f"ID: {expense.expense_id}, Date: {expense.date}, Amount: {expense.amount}, Category: {expense.category}, Description: {expense.description}")
            expense_id = int(input("Enter expense ID to update: "))
            date_str = input("New date (YYYY-MM-DD, leave blank to keep current): ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
            amount = input("New amount (leave blank to keep current): ")
            amount = float(amount) if amount else None
            category = input("New category (leave blank to keep current): ")
            description = input("New description (leave blank to keep current): ")
            update_expense(expense_id, authenticated_user, date, amount, category, description)
        elif choice == '3':
            print("\nYour Expenses:")
            expenses = get_expense_report_by_username(authenticated_user)
            for expense in expenses:
                print(f"ID: {expense.expense_id}, Date: {expense.date}, Amount: {expense.amount}, Category: {expense.category}, Description: {expense.description}")
            expense_id = int(input("Enter expense ID to delete: "))
            delete_expense(expense_id, authenticated_user)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def inventory_management():
    while True:
        print("\nInventory Management")
        print("1. Add Inventory Item")
        print("2. Update Inventory Item")
        print("3. Delete Inventory Item")
        print("4. Back to Main Menu")

        choice = input("Select an option (1-4): ")

        if choice == '1':
            item_name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            cost = float(input("Enter cost per unit: "))
            add_inventory_item(authenticated_user, item_name, quantity, cost)
        elif choice == '2':
            print("\nYour Inventory Items:")
            inventory = get_inventory_report(authenticated_user)
            for item in inventory:
                print(f"ID: {item.item_id}, Name: {item.item_name}, Quantity: {item.quantity}, Cost: {item.cost}")
            item_id = int(input("Enter inventory item ID to update: "))
            item_name = input("New item name (leave blank to keep current): ")
            quantity = input("New quantity (leave blank to keep current): ")
            quantity = int(quantity) if quantity else None
            cost = input("New cost per unit (leave blank to keep current): ")
            cost = float(cost) if cost else None
            update_inventory(item_id, item_name=item_name or None, quantity=quantity, cost=cost)
        elif choice == '3':
            print("\nYour Inventory Items:")
            inventory = get_inventory_report(authenticated_user)
            for item in inventory:
                print(f"ID: {item.item_id}, Name: {item.item_name}, Quantity: {item.quantity}, Cost: {item.cost}")
            item_id = int(input("Enter inventory item ID to delete: "))
            delete_inventory(item_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def sales_management():
    while True:
        print("\nSales Management")
        print("1. Record Sale")
        print("2. Update Sale")
        print("3. Delete Sale")
        print("4. Back to Main Menu")

        choice = input("Select an option (1-4): ")

        if choice == '1':
            date_str = input("Enter date (YYYY-MM-DD): ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            total_amount = float(input("Enter total amount: "))
            items_sold = input("Enter items sold (e.g., '2x Coffee, 1x Muffin'): ")
            record_sale(authenticated_user, date, total_amount, items_sold)
        elif choice == '2':
            print("\nYour Sales:")
            sales = get_sales_report_by_username(authenticated_user)
            for sale in sales:
                print(f"ID: {sale.sale_id}, Date: {sale.date}, Total Amount: {sale.total_amount}, Items Sold: {sale.items_sold}")
            sale_id = int(input("Enter sale ID to update: "))
            date_str = input("New date (YYYY-MM-DD, leave blank to keep current): ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
            total_amount = input("New total amount (leave blank to keep current): ")
            total_amount = float(total_amount) if total_amount else None
            items_sold = input("New items sold (leave blank to keep current): ")
            update_sale(sale_id, authenticated_user, date, total_amount, items_sold)
        elif choice == '3':
            print("\nYour Sales:")
            sales = get_sales_report_by_username(authenticated_user)
            for sale in sales:
                print(f"ID: {sale.sale_id}, Date: {sale.date}, Total Amount: {sale.total_amount}, Items Sold: {sale.items_sold}")
            sale_id = int(input("Enter sale ID to delete: "))
            delete_sale(sale_id, authenticated_user)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def reports_menu():
    while True:
        print("\nReports")
        print("1. View Expense Report")
        print("2. View Sales Report")
        print("3. View Inventory Report")
        print("4. Back to Main Menu")

        choice = input("Select an option (1-4): ")

        if choice == '1':
            expenses = get_expense_report_by_username(authenticated_user)
            print("\nExpense Report:")
            for expense in expenses:
                print(f"Date: {expense.date}, Amount: {expense.amount}, Category: {expense.category}, Description: {expense.description}")
        elif choice == '2':
            sales = get_sales_report_by_username(authenticated_user)
            print("\nSales Report:")
            for sale in sales:
                print(f"Date: {sale.date}, Total Amount: {sale.total_amount}, Items Sold: {sale.items_sold}")
        elif choice == '3':
            inventory = get_inventory_report(authenticated_user)
            print("\nInventory Report:")
            for item in inventory:
                print(f"Item Name: {item.item_name}, Quantity: {item.quantity}, Cost: {item.cost}")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
