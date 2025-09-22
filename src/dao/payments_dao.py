from typing import Optional, Dict
from src.config import get_supabase

def _sb():
    return get_supabase()

def create_payment(order_id: int, amount: float) -> Optional[Dict]:
    data = {"order_id": order_id, "amount": amount, "status": "PENDING"}
    res = _sb().table("payments").insert(data).execute()
    return res.data[0] if res.data else None

def process_payment(order_id: int, method: str) -> Optional[Dict]:
    res = _sb().table("payments").update({"status": "PAID", "method": method}).eq("order_id", order_id).execute()
    if not res.data:
        return None
    _sb().table("orders").update({"status": "COMPLETED"}).eq("order_id", order_id).execute()
    return res.data[0]

def refund_payment(order_id: int) -> Optional[Dict]:
    res = _sb().table("payments").update({"status": "REFUNDED"}).eq("order_id", order_id).execute()
    if not res.data:
        return None
    _sb().table("orders").update({"status": "CANCELLED"}).eq("order_id", order_id).execute()
    return res.data[0]

def get_payment(order_id: int) -> Optional[Dict]:
    res = _sb().table("payments").select("*").eq("order_id", order_id).limit(1).execute()
    return res.data[0] if res.data else None
