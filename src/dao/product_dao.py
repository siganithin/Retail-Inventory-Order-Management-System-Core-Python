# src/dao/product_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase

def _sb():
    """Get Supabase client."""
    return get_supabase()

def create_product(name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Optional[Dict]:
    """Insert a new product into the database."""
    payload = {"name": name, "sku": sku, "price": price, "stock": stock}
    if category:
        payload["category"] = category

    _sb().table("products").insert(payload).execute()
    resp = _sb().table("products").select("*").eq("sku", sku).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_product_by_id(prod_id: int) -> Optional[Dict]:
    """Fetch a product by its ID."""
    resp = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_product_by_sku(sku: str) -> Optional[Dict]:
    """Fetch a product by its SKU."""
    resp = _sb().table("products").select("*").eq("sku", sku).limit(1).execute()
    return resp.data[0] if resp.data else None

def update_product(prod_id: int, fields: Dict) -> Optional[Dict]:
    """Update product fields."""
    _sb().table("products").update(fields).eq("prod_id", prod_id).execute()
    resp = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def list_products(limit: int = 100, category: str | None = None) -> List[Dict]:
    """List products, optionally filtered by category."""
    q = _sb().table("products").select("*").order("prod_id", desc=False).limit(limit)
    if category:
        q = q.eq("category", category)
    resp = q.execute()
    return resp.data or []

def update_stock(prod_id: int, delta: int) -> Optional[Dict]:
    """
    Update stock for a product.
    Delta can be negative (deduct) or positive (restore).
    """
    product = get_product_by_id(prod_id)
    if not product:
        raise ValueError(f"Product not found: {prod_id}")

    new_stock = product["stock"] + delta
    if new_stock < 0:
        raise ValueError("Stock cannot be negative")

    res = _sb().table("products").update({"stock": new_stock}).eq("prod_id", prod_id).execute()
    return res.data[0] if res.data else None
