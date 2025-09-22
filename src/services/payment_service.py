from typing import Optional, Dict
from src.dao import payments_dao

def create_payment_for_order(order_id: int, total_amount: float) -> Optional[Dict]:
    return payments_dao.create_payment(order_id, total_amount)

def pay_order(order_id: int, method: str) -> Optional[Dict]:
    return payments_dao.process_payment(order_id, method)

def refund_order(order_id: int) -> Optional[Dict]:
    return payments_dao.refund_payment(order_id)

def get_payment_details(order_id: int) -> Optional[Dict]:
    return payments_dao.get_payment(order_id)
