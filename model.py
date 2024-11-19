from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import bcrypt
from datetime import datetime

Base = declarative_base()

engine = create_engine('sqlite:///expense_tracking.db')
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    expenses = relationship("Expense", back_populates="user")
    sales = relationship("Sale", back_populates="user")
    inventory_items = relationship("Inventory", back_populates="user")

class Expense(Base):
    __tablename__ = 'Expenses'

    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    date = Column(Date, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)

    user = relationship("User", back_populates="expenses")

class Inventory(Base):
    __tablename__ = 'Inventory'

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    item_name = Column(String, nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)

    user = relationship("User", back_populates="inventory_items")

class Sale(Base):
    __tablename__ = 'Sales'

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    date = Column(Date, nullable=False, index=True)
    total_amount = Column(Float, nullable=False)
    items_sold = Column(String, nullable=False)

    user = relationship("User", back_populates="sales")

Base.metadata.create_all(engine)

def add_user(username, password, email):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password=hashed_password.decode('utf-8'), email=email)
    session.add(new_user)
    session.commit()

def authenticate_user(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user
    return None

def update_user(user_id, username=None, password=None, email=None):
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        if username:
            user.username = username
        if password:
            user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        if email:
            user.email = email
        session.commit()

def delete_user(user_id):
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        session.delete(user)
        session.commit()

def add_expense(user_id, date, amount, category, description=""):
    new_expense = Expense(user_id=user_id, date=date, amount=amount, category=category, description=description)
    session.add(new_expense)
    session.commit()

def update_expense(expense_id, date=None, amount=None, category=None, description=None):
    expense = session.query(Expense).filter_by(expense_id=expense_id).first()
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

def delete_expense(expense_id):
    expense = session.query(Expense).filter_by(expense_id=expense_id).first()
    if expense:
        session.delete(expense)
        session.commit()

def add_inventory_item(item_name, quantity, cost):
    new_item = Inventory(item_name=item_name, quantity=quantity, cost=cost)
    session.add(new_item)
    session.commit()

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

def delete_inventory(item_id):
    item = session.query(Inventory).filter_by(item_id=item_id).first()
    if item:
        session.delete(item)
        session.commit()

def add_sale(user_id, date, total_amount, items_sold):
    new_sale = Sale(user_id=user_id, date=date, total_amount=total_amount, items_sold=items_sold)
    session.add(new_sale)
    session.commit()

def update_sale(sale_id, date=None, total_amount=None, items_sold=None):
    sale = session.query(Sale).filter_by(sale_id=sale_id).first()
    if sale:
        if date:
            sale.date = date
        if total_amount:
            sale.total_amount = total_amount
        if items_sold:
            sale.items_sold = items_sold
        session.commit()

def delete_sale(sale_id):
    sale = session.query(Sale).filter_by(sale_id=sale_id).first()
    if sale:
        session.delete(sale)
        session.commit()
