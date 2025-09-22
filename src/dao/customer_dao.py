from typing import List, Dict, Optional
from src.config import get_supabase

def _sb():
    return get_supabase()

def create_customer(name: str, email: str, phone: str, city: str | None = None) -> Optional[Dict]:
    existing = _sb().table("customers").select("*").eq("email", email).limit(1).execute()
    if existing.data:
        raise ValueError(f"Email already exists: {email}")

    payload = {"name": name, "email": email, "phone": phone}
    if city:
        payload["city"] = city
    _sb().table("customers").insert(payload).execute()

    resp = _sb().table("customers").select("*").eq("email", email).limit(1).execute()
    return resp.data[0] if resp.data else None

def update_customer(cust_id: int, fields: Dict) -> Optional[Dict]:
    _sb().table("customers").update(fields).eq("cust_id", cust_id).execute()
    resp = _sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def delete_customer(cust_id: int) -> Optional[Dict]:
    orders = _sb().table("orders").select("*").eq("cust_id", cust_id).limit(1).execute()
    if orders.data:
        raise ValueError("Cannot delete: customer has orders")

    resp_before = _sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    row = resp_before.data[0] if resp_before.data else None
    _sb().table("customers").delete().eq("cust_id", cust_id).execute()
    return row

def list_customers(limit: int = 100) -> List[Dict]:
    resp = _sb().table("customers").select("*").order("cust_id").limit(limit).execute()
    return resp.data or []

def search_customers(email: str | None = None, city: str | None = None) -> List[Dict]:
    q = _sb().table("customers").select("*")
    if email:
        q = q.eq("email", email)
    if city:
        q = q.eq("city", city)
    resp = q.execute()
    return resp.data or []

def get_customer_by_id(cust_id: int):
    res = _sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    return res.data[0] if res.data else None
