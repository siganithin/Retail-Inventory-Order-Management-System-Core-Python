from typing import List, Dict, Optional
from src.config import get_supabase

def _sb():
    return get_supabase()

def insert_order(customer_id: int, total_amount: float) -> Optional[Dict]:
    data = {"cust_id": customer_id, "total_amount": total_amount, "status": "PLACED"}
    res = _sb().table("orders").insert(data).execute()
    return res.data[0] if res.data else None

def insert_order_items(order_id: int, items: List[Dict]) -> List[Dict]:
    data = [{"order_id": order_id, "prod_id": i["prod_id"], "quantity": i["quantity"]} for i in items]
    res = _sb().table("order_items").insert(data).execute()
    return res.data or []

def fetch_order_by_id(order_id: int) -> Optional[Dict]:
    res = _sb().table("orders").select("*").eq("order_id", order_id).limit(1).execute()
    return res.data[0] if res.data else None

def fetch_order_items(order_id: int) -> List[Dict]:
    res = _sb().table("order_items").select("*").eq("order_id", order_id).execute()
    return res.data or []

def fetch_order_details(order_id: int) -> Optional[Dict]:
    order = fetch_order_by_id(order_id)
    if not order:
        return None
    items = fetch_order_items(order_id)
    return {**order, "items": items}

def fetch_orders(customer_id: int | None = None) -> List[Dict]:
    q = _sb().table("orders").select("*")
    if customer_id:
        q = q.eq("cust_id", customer_id)
    return q.execute().data or []

def update_order_status(order_id: int, status: str) -> Optional[Dict]:
    res = _sb().table("orders").update({"status": status}).eq("order_id", order_id).execute()
    return res.data[0] if res.data else None
