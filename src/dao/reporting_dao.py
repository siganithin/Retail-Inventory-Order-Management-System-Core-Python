# src/dao/reporting_dao.py
from datetime import datetime, timedelta
from src.config import get_supabase

def _sb():
    return get_supabase()

# Top 5 selling products by total quantity
def top_selling_products(limit=5):
    res = _sb().table("order_items").select("prod_id, quantity").execute()
    items = res.data or []

    # Aggregate quantity per product
    agg = {}
    for i in items:
        pid = i["prod_id"]
        qty = i["quantity"]
        agg[pid] = agg.get(pid, 0) + qty

    # Sort descending by total quantity
    sorted_items = sorted(agg.items(), key=lambda x: x[1], reverse=True)[:limit]

    # Fetch product names
    products = []
    for pid, total_qty in sorted_items:
        prod = _sb().table("products").select("name").eq("prod_id", pid).limit(1).execute()
        name = prod.data[0]["name"] if prod.data else f"Product {pid}"
        products.append({"prod_id": pid, "name": name, "total_qty": total_qty})

    return products

# Total revenue in the last month
def total_revenue_last_month():
    today = datetime.utcnow()
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_last_month = today.replace(day=1) - timedelta(days=1)

    res = _sb().table("orders")\
        .select("total_amount")\
        .gte("created_at", first_day_last_month.isoformat())\
        .lte("created_at", last_day_last_month.isoformat())\
        .execute()

    orders = res.data or []
    total_revenue = sum(o["total_amount"] for o in orders)
    return {"total_revenue_last_month": total_revenue}

# Total orders placed by each customer
def total_orders_by_customer():
    res = _sb().table("orders").select("cust_id").execute()
    orders = res.data or []

    agg = {}
    for o in orders:
        cid = o["cust_id"]
        agg[cid] = agg.get(cid, 0) + 1

    # Fetch customer names
    result = []
    for cid, total_orders in agg.items():
        cust = _sb().table("customers").select("name").eq("cust_id", cid).limit(1).execute()
        name = cust.data[0]["name"] if cust.data else f"Customer {cid}"
        result.append({"cust_id": cid, "name": name, "total_orders": total_orders})

    return result

# Customers who placed more than 2 orders
def frequent_customers(min_orders=2):
    all_orders = total_orders_by_customer()
    return [c for c in all_orders if c["total_orders"] > min_orders]
