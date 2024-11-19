from model import session, User, Expense, Inventory, Sale, add_user, authenticate_user
from datetime import datetime

authenticated_user = None

def register_user(username, password, email):
    existing_user = session.query(User).filter_by(username=username).first()
    existing_email = session.query(User).filter_by(email=email).first()

    if existing_user:
        print(f"Username '{username}' is already taken.")
        return False
    if existing_email:
        print(f"Email '{email}' is already registered.")
        return False

    add_user(username, password, email)
    print(f"User '{username}' registered successfully.")
    return True

def login_user(username, password):
    global authenticated_user
    user = authenticate_user(username, password)
    if user:
        authenticated_user = user.username
        print(f"User '{username}' logged in successfully.")
        return True
    print("Invalid username or password.")
    return False

def logout_user():
    global authenticated_user
    print(f"User '{authenticated_user}' logged out.")
    authenticated_user = None

def check_authentication(username):
    if authenticated_user != username:
        print(f"Unauthorized access by '{authenticated_user}'.")
        return False
    return True

def record_expense(username, date, amount, category, description=""):
    if not check_authentication(username):
        return False
    expense = Expense(user_id=session.query(User).filter_by(username=username).first().user_id,
                      date=date, amount=amount, category=category, description=description)
    session.add(expense)
    session.commit()
    print(f"Expense recorded for user '{username}'.")
    return True

def update_expense(expense_id, username, date=None, amount=None, category=None, description=None):
    if not check_authentication(username):
        return False
    expense = session.query(Expense).filter_by(expense_id=expense_id, user_id=session.query(User).filter_by(username=username).first().user_id).first()
    if expense:
        if date:
            expense.date = date
        if amount:
            expense.amount = amount
        if category:
            expense.category = category
        if description:
            expense.description = description
        session.commit()
        print(f"Expense '{expense_id}' updated successfully.")
        return True
    print(f"Expense '{expense_id}' not found.")
    return False

def delete_expense(expense_id, username):
    if not check_authentication(username):
        return False
    expense = session.query(Expense).filter_by(expense_id=expense_id, user_id=session.query(User).filter_by(username=username).first().user_id).first()
    if expense:
        session.delete(expense)
        session.commit()
        print(f"Expense '{expense_id}' deleted successfully.")
        return True
    print(f"Expense '{expense_id}' not found.")
    return False

def add_inventory_item(username, item_name, quantity, cost):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print("User not found.")
        return False
    new_item = Inventory(user_id=user.user_id, item_name=item_name, quantity=quantity, cost=cost)
    session.add(new_item)
    session.commit()
    print(f"Inventory item '{item_name}' added successfully.")
    return True

def update_inventory(item_id, item_name=None, quantity=None, cost=None):
    item = session.query(Inventory).filter_by(item_id=item_id).first()
    if item:
        if item_name:
            item.item_name = item_name
        if quantity:
            item.quantity = quantity
        if cost:
            item.cost = cost
        session.commit()
        print(f"Inventory item '{item_id}' updated successfully.")
        return True
    print(f"Inventory item '{item_id}' not found.")
    return False

def delete_inventory(item_id):
    item = session.query(Inventory).filter_by(item_id=item_id).first()
    if item:
        session.delete(item)
        session.commit()
        print(f"Inventory item '{item_id}' deleted successfully.")
        return True
    print(f"Inventory item '{item_id}' not found.")
    return False

def record_sale(username, date, total_amount, items_sold):
    if not check_authentication(username):
        return False
    sale = Sale(user_id=session.query(User).filter_by(username=username).first().user_id,
                date=date, total_amount=total_amount, items_sold=items_sold)
    session.add(sale)
    session.commit()
    print(f"Sale recorded for user '{username}'.")
    return True

def update_sale(sale_id, username, date=None, total_amount=None, items_sold=None):
    if not check_authentication(username):
        return False
    sale = session.query(Sale).filter_by(sale_id=sale_id, user_id=session.query(User).filter_by(username=username).first().user_id).first()
    if sale:
        if date:
            sale.date = date
        if total_amount:
            sale.total_amount = total_amount
        if items_sold:
            sale.items_sold = items_sold
        session.commit()
        print(f"Sale '{sale_id}' updated successfully.")
        return True
    print(f"Sale '{sale_id}' not found.")
    return False

def delete_sale(sale_id, username):
    if not check_authentication(username):
        return False
    sale = session.query(Sale).filter_by(sale_id=sale_id, user_id=session.query(User).filter_by(username=username).first().user_id).first()
    if sale:
        session.delete(sale)
        session.commit()
        print(f"Sale '{sale_id}' deleted successfully.")
        return True
    print(f"Sale '{sale_id}' not found.")
    return False

def get_expense_report_by_username(username):
    if not check_authentication(username):
        return []
    expenses = session.query(Expense).filter_by(user_id=session.query(User).filter_by(username=username).first().user_id).all()
    return expenses

def get_sales_report_by_username(username):
    if not check_authentication(username):
        return []
    sales = session.query(Sale).filter_by(user_id=session.query(User).filter_by(username=username).first().user_id).all()
    return sales

def get_inventory_report(username):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print("User not found.")
        return []
    inventory_items = session.query(Inventory).filter_by(user_id=user.user_id).all()
    if not inventory_items:
        print("No inventory items found for this user.")
        return []
    return inventory_items
