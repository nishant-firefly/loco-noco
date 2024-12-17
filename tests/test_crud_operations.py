from src.models.models import User, Product, Order
from src.utils.data_loader import DataLoader
from sqlalchemy.sql import func

def test_crud_operations(db_helper):
    """
    Perform CRUD operations and complex queries.
    """
    session = db_helper.get_session()

    # Load data using DataLoader
    loader = DataLoader()
    users_data = loader.load_data(sheet_name="users")
    products_data = loader.load_data(sheet_name="products")
    orders_data = loader.load_data(sheet_name="orders")

    # Clear existing data to avoid duplicate key issues
    session.query(Order).delete()
    session.query(Product).delete()
    session.query(User).delete()
    session.commit()

    # Insert Users
    users = [
        User(id=row['id'], name=row['name'], age=row['age'])
        for _, row in users_data.iterrows()
    ]
    session.add_all(users)

    # Insert Products
    products = [
        Product(id=row['id'], name=row['name'], price=row['price'])
        for _, row in products_data.iterrows()
    ]
    session.add_all(products)

    # Insert Orders
    orders = [
        Order(
            id=int(row['id']),
            user_id=int(row['user_id']),
            product_id=int(row['product_id']),
            quantity=int(row['quantity'])
        )
        for _, row in orders_data.iterrows()
    ]
    session.add_all(orders)

    # Commit data to the database
    session.commit()

    # ===== CRUD Operation Tests =====

    # Read all Users
    users = session.query(User).all()
    assert len(users) > 0, "No users found in the database."

    # Read Products priced greater than 500
    expensive_products = session.query(Product).filter(Product.price > 500).all()
    assert len(expensive_products) > 0, "No products priced above 500 found."

    # Join Users and Orders
    user_orders = session.query(User.name, Product.name, Order.quantity) \
        .join(Order, User.id == Order.user_id) \
        .join(Product, Product.id == Order.product_id) \
        .all()
    assert len(user_orders) > 0, "No user orders found in the database."

    # Group by user and calculate total quantity of orders
    total_quantity = session.query(User.name, func.sum(Order.quantity).label('total_quantity')) \
        .join(Order, User.id == Order.user_id) \
        .group_by(User.name) \
        .all()
    assert len(total_quantity) > 0, "No aggregated order quantities found."

    # Paginate orders
    page = 1
    page_size = 1
    paginated_orders = session.query(Order).limit(page_size).offset((page - 1) * page_size).all()
    assert len(paginated_orders) == page_size, "Pagination did not return the correct number of orders."

    # ===== Clean up =====
    session.close()
