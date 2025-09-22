import argparse
import json

from src.services import product_service, order_service, payment_service
from src.dao import product_dao, customer_dao, reporting_dao


def cmd_product_add(args):
    try:
        p = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_list(args):
    ps = product_dao.list_products(limit=100)
    print(json.dumps(ps, indent=2, default=str))

def cmd_customer_add(args):
    try:
        c = customer_dao.create_customer(args.name, args.email, args.phone, args.city)
        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_update(args):
    try:
        fields = {}
        if args.phone:
            fields["phone"] = args.phone
        if args.city:
            fields["city"] = args.city
        c = customer_dao.update_customer(args.customer, fields)
        print("Updated customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_delete(args):
    try:
        c = customer_dao.delete_customer(args.customer)
        print("Deleted customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_list(args):
    cs = customer_dao.list_customers(limit=100)
    print(json.dumps(cs, indent=2, default=str))

def cmd_customer_search(args):
    cs = customer_dao.search_customers(email=args.email, city=args.city)
    print(json.dumps(cs, indent=2, default=str))

def cmd_order_create(args):
    items = []
    for item in args.item:
        try:
            pid, qty = item.split(":")
            items.append({"prod_id": int(pid), "quantity": int(qty)})
        except Exception:
            print("Invalid item format:", item)
            return
    try:
        ord = order_service.create_order(args.customer, items)
        print("Order created:")
        print(json.dumps(ord, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_show(args):
    try:
        o = order_service.get_order_details(args.order)
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_cancel(args):
    try:
        o = order_service.cancel_order(args.order)
        print("Order cancelled (updated):")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_payment_process(args):
    try:
        p = payment_service.pay_order(args.order, args.method)
        print("Payment processed:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_payment_refund(args):
    try:
        r = payment_service.refund_order(args.order)
        print("Payment refunded:")
        print(json.dumps(r, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_report_top_products(args):
    r = reporting_dao.top_selling_products()
    print(json.dumps(r, indent=2, default=str))

def cmd_report_total_revenue(args):
    r = reporting_dao.total_revenue_last_month()
    print(json.dumps(r, indent=2, default=str))

def cmd_report_orders_by_customer(args):
    r = reporting_dao.total_orders_by_customer()
    print(json.dumps(r, indent=2, default=str))

def cmd_report_frequent_customers(args):
    r = reporting_dao.frequent_customers()
    print(json.dumps(r, indent=2, default=str))

def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")


    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    pcust = sub.add_parser("customer", help="customer commands")
    pcust_sub = pcust.add_subparsers(dest="action")
    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)
    updatec = pcust_sub.add_parser("update")
    updatec.add_argument("--customer", type=int, required=True)
    updatec.add_argument("--phone", default=None)
    updatec.add_argument("--city", default=None)
    updatec.set_defaults(func=cmd_customer_update)
    deletec = pcust_sub.add_parser("delete")
    deletec.add_argument("--customer", type=int, required=True)
    deletec.set_defaults(func=cmd_customer_delete)
    listc = pcust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)
    searchc = pcust_sub.add_parser("search")
    searchc.add_argument("--email", default=None)
    searchc.add_argument("--city", default=None)
    searchc.set_defaults(func=cmd_customer_search)

  
    porder = sub.add_parser("order", help="order commands")
    porder_sub = porder.add_subparsers(dest="action")
    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
    createo.set_defaults(func=cmd_order_create)
    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)
    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)

    ppay = sub.add_parser("payment", help="payment commands")
    ppay_sub = ppay.add_subparsers(dest="action")
    pay_process = ppay_sub.add_parser("process")
    pay_process.add_argument("--order", type=int, required=True)
    pay_process.add_argument("--method", type=str, choices=["Cash","Card","UPI"], required=True)
    pay_process.set_defaults(func=cmd_payment_process)
    pay_refund = ppay_sub.add_parser("refund")
    pay_refund.add_argument("--order", type=int, required=True)
    pay_refund.set_defaults(func=cmd_payment_refund)

    
    prep = sub.add_parser("report", help="reporting commands")
    prep_sub = prep.add_subparsers(dest="action")
    top_prod = prep_sub.add_parser("top_products")
    top_prod.set_defaults(func=cmd_report_top_products)
    total_rev = prep_sub.add_parser("revenue_last_month")
    total_rev.set_defaults(func=cmd_report_total_revenue)
    orders_by_cust = prep_sub.add_parser("orders_by_customer")
    orders_by_cust.set_defaults(func=cmd_report_orders_by_customer)
    freq_cust = prep_sub.add_parser("frequent_customers")
    freq_cust.set_defaults(func=cmd_report_frequent_customers)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
