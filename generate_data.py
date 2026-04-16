import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ── Customers (includes NULLs for join edge cases) ──
customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"],
    "city": ["New York", "London", "New York", "Paris", None, "London", "Tokyo", None, "Paris", "New York"],
    "segment": ["Enterprise", "SMB", "Enterprise", "SMB", "Enterprise", "Mid-Market", "SMB", "Enterprise", "Mid-Market", "SMB"],
    "signup_date": ["2023-01-15", "2023-02-20", "2023-01-10", "2023-03-05", "2023-04-12", "2023-05-01", "2023-06-18", "2023-02-28", "2023-07-22", "2023-08-10"],
    "referrer_id": [None, 1, None, 2, 3, None, 4, 1, None, 5],
})

# ── Products ──
products = pd.DataFrame({
    "product_id": [101, 102, 103, 104, 105, 106],
    "product_name": ["Widget A", "Widget B", "Gadget X", "Gadget Y", "Service Plan S", "Service Plan M"],
    "category": ["Widgets", "Widgets", "Gadgets", "Gadgets", "Services", "Services"],
    "unit_price": [25.00, 45.00, 150.00, 200.00, 9.99, 29.99],
    "launch_date": ["2022-06-01", "2022-09-15", "2023-01-01", "2023-03-01", "2022-01-01", "2022-01-01"],
})

# ── Orders (some customers have no orders; some orders reference NULL discount) ──
orders = pd.DataFrame({
    "order_id": list(range(1001, 1026)),
    "customer_id": [1,1,2,3,3,3,4,5,6,6,7,7,7,8,9,10,10,1,2,4,5,6,8,9,10],
    "order_date": [
        "2023-01-20","2023-03-15","2023-02-25","2023-01-18","2023-04-10","2023-06-30",
        "2023-03-12","2023-05-01","2023-05-10","2023-07-20","2023-06-25","2023-08-05","2023-09-15",
        "2023-03-05","2023-08-01","2023-08-15","2023-09-20","2023-10-05","2023-10-15","2023-11-01",
        "2023-11-10","2023-11-20","2023-12-01","2023-12-10","2023-12-20",
    ],
    "status": [
        "completed","completed","completed","completed","completed","completed",
        "completed","cancelled","completed","completed","completed","completed","returned",
        "completed","completed","completed","completed","completed","cancelled","completed",
        "completed","completed","completed","completed","completed",
    ],
    "discount_pct": [
        0,10,0,5,5,0,None,0,15,0,0,10,0,None,0,5,0,20,None,0,0,10,0,5,0
    ],
})

# ── Order Items ──
order_items = pd.DataFrame({
    "item_id": list(range(1, 41)),
    "order_id": [
        1001,1001,1002,1003,1004,1004,1005,1006,1006,1007,
        1008,1009,1009,1010,1011,1012,1012,1013,1014,1015,
        1016,1016,1017,1018,1018,1019,1020,1021,1022,1022,
        1023,1024,1024,1025,1025,1001,1003,1007,1011,1015,
    ],
    "product_id": [
        101,102,103,101,102,104,101,103,105,104,
        106,101,102,103,105,101,106,104,102,103,
        101,105,102,103,104,106,101,102,103,105,
        104,101,106,102,103,101,105,106,101,104,
    ],
    "quantity": [
        2,1,1,3,2,1,4,1,2,1,
        3,5,1,2,1,2,1,1,3,1,
        4,2,1,2,1,1,3,2,1,3,
        1,4,2,2,1,1,1,2,3,1,
    ],
})

# ── Employees (for self-join / hierarchy) ──
employees = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5, 6, 7],
    "name": ["CEO Sara", "VP Mark", "VP Lisa", "Mgr Tom", "Mgr Amy", "Dev Joe", "Dev Kim"],
    "manager_id": [None, 1, 1, 2, 3, 4, 4],
    "department": ["Exec", "Sales", "Engineering", "Sales", "Engineering", "Sales", "Sales"],
    "salary": [250000, 180000, 180000, 120000, 130000, 90000, 95000],
})

# ── Monthly Metrics (for window functions / running totals) ──
months = []
for cid in [1, 2, 3]:
    for m in range(1, 13):
        import random; random.seed(cid * 100 + m)
        months.append({
            "customer_id": cid,
            "month": f"2023-{m:02d}-01",
            "monthly_revenue": round(random.uniform(500, 5000), 2),
            "support_tickets": random.randint(0, 10),
        })
monthly_metrics = pd.DataFrame(months)

# ── Save all CSVs ──
for name, df in [
    ("customers", customers),
    ("products", products),
    ("orders", orders),
    ("order_items", order_items),
    ("employees", employees),
    ("monthly_metrics", monthly_metrics),
]:
    df.to_csv(os.path.join(DATA_DIR, f"{name}.csv"), index=False)
    print(f"Created {name}.csv  ({len(df)} rows)")

print("\nAll CSV files generated in", DATA_DIR)

