from src.dao import customer_dao, product_dao, order_dao
def create_order(customer_id, items):
    # 1. Check customer exists
    customer = customer_dao.get_customer_by_id(customer_id)
    if not customer:
        raise ValueError(f"Customer {customer_id} not found")

    total_amount = 0
    # 2. Check stock for all products
    for item in items:
        product = product_dao.get_product_by_id(item["prod_id"])
        if not product:
            raise ValueError(f"Product {item['prod_id']} not found")
        if product["stock"] < item["quantity"]:
            raise ValueError(f"Not enough stock for product {product['name']}")
        total_amount += product["price"] * item["quantity"]

    # 3. Deduct stock
    for item in items:
        product_dao.update_stock(item["prod_id"], -item["quantity"])

    # 4. Insert order + order items
    order = order_dao.insert_order(customer_id, total_amount)
    order_items = order_dao.insert_order_items(order["id"], items)

    return {
        "order": order,
        "items": order_items,
        "customer": customer
    }

def get_order_details(order_id):
    return order_dao.fetch_order_details(order_id)

def list_orders(customer_id=None):
    return order_dao.fetch_orders(customer_id)

def cancel_order(order_id):
    order = order_dao.fetch_order_by_id(order_id)
    if not order:
        raise ValueError("Order not found")
    if order["status"] != "PLACED":
        raise ValueError("Only PLACED orders can be cancelled")

    items = order_dao.fetch_order_items(order_id)
    for item in items:
        product_dao.update_stock(item["prod_id"], item["quantity"])

    return order_dao.update_order_status(order_id, "CANCELLED")

def mark_order_completed(order_id):
    return order_dao.update_order_status(order_id, "COMPLETED")


def create_order(customer_id, items):
    customer = customer_dao.get_customer_by_id(customer_id)
    if not customer:
        raise ValueError(f"Customer not found: {customer_id}")
