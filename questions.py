QUESTIONS = [
    # ── JOIN Edge Cases ──
    {
        "id": 1,
        "topic": "JOIN Edge Cases",
        "difficulty": "Easy",
        "title": "Inner Join – Customers with Orders",
        "question": "List all customers who have placed at least one order. Show customer_id, name, and order_id.",
        "hint": "Use INNER JOIN between customers and orders.",
        "answer": """SELECT c.customer_id, c.name, o.order_id
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;""",
    },
    {
        "id": 2,
        "topic": "JOIN Edge Cases",
        "difficulty": "Easy",
        "title": "Left Join – Customers WITHOUT Orders",
        "question": "Find customers who have NEVER placed an order. Show customer_id and name.",
        "hint": "LEFT JOIN + WHERE … IS NULL",
        "answer": """SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;""",
    },
    {
        "id": 3,
        "topic": "JOIN Edge Cases",
        "difficulty": "Medium",
        "title": "Self Join – Customer Referrals",
        "question": "Show each customer and the name of the person who referred them. Include customers with no referrer (show NULL).",
        "hint": "Self LEFT JOIN on customers using referrer_id.",
        "answer": """SELECT c.customer_id, c.name, r.name AS referrer_name
FROM customers c
LEFT JOIN customers r ON c.referrer_id = r.customer_id
ORDER BY c.customer_id;""",
    },
    {
        "id": 4,
        "topic": "JOIN Edge Cases",
        "difficulty": "Medium",
        "title": "NULLs in Joins – Orders with NULL Discount",
        "question": "List orders where discount_pct IS NULL. Show order_id, customer name, and discount_pct.",
        "hint": "JOIN orders and customers, filter WHERE discount_pct IS NULL.",
        "answer": """SELECT o.order_id, c.name, o.discount_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.discount_pct IS NULL;""",
    },
    {
        "id": 5,
        "topic": "JOIN Edge Cases",
        "difficulty": "Hard",
        "title": "Full Outer Join Simulation",
        "question": "Show ALL customers and ALL orders, even if they don't match. Use a FULL OUTER JOIN.",
        "hint": "DuckDB supports FULL OUTER JOIN directly.",
        "answer": """SELECT c.customer_id, c.name, o.order_id, o.order_date
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;""",
    },

    # ── Revenue & Aggregation ──
    {
        "id": 6,
        "topic": "Revenue & Aggregation",
        "difficulty": "Medium",
        "title": "Revenue Calculation",
        "question": "Calculate total revenue per order (quantity × unit_price) for completed orders only. Apply discount_pct where available (treat NULL as 0).",
        "hint": "JOIN orders, order_items, products. Use COALESCE for NULL discounts.",
        "answer": """SELECT o.order_id,
       ROUND(SUM(oi.quantity * p.unit_price * (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY o.order_id
ORDER BY total_revenue DESC;""",
    },
    {
        "id": 7,
        "topic": "Revenue & Aggregation",
        "difficulty": "Medium",
        "title": "Customer-Level Aggregation",
        "question": "For each customer, show total orders, total revenue, and average order value. Only count completed orders.",
        "hint": "Group by customer after joining all relevant tables.",
        "answer": """SELECT c.customer_id, c.name,
       COUNT(DISTINCT o.order_id) AS total_orders,
       ROUND(SUM(oi.quantity * p.unit_price * (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS total_revenue,
       ROUND(SUM(oi.quantity * p.unit_price * (1 - COALESCE(o.discount_pct, 0) / 100.0)) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY total_revenue DESC;""",
    },
    {
        "id": 8,
        "topic": "Revenue & Aggregation",
        "difficulty": "Medium",
        "title": "Top-3 Customers by Revenue",
        "question": "Show the top 3 customers by total revenue from completed orders.",
        "hint": "Use the previous revenue query with LIMIT 3.",
        "answer": """SELECT c.customer_id, c.name,
       ROUND(SUM(oi.quantity * p.unit_price * (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY total_revenue DESC
LIMIT 3;""",
    },
    {
        "id": 9,
        "topic": "Revenue & Aggregation",
        "difficulty": "Medium",
        "title": "Conditional Aggregation – Revenue by Category",
        "question": "Show total revenue broken down by product category using CASE expressions. Columns: customer_id, widgets_revenue, gadgets_revenue, services_revenue.",
        "hint": "SUM(CASE WHEN category = '...' THEN ... END)",
        "answer": """SELECT c.customer_id, c.name,
       ROUND(SUM(CASE WHEN p.category = 'Widgets' THEN oi.quantity * p.unit_price ELSE 0 END), 2) AS widgets_revenue,
       ROUND(SUM(CASE WHEN p.category = 'Gadgets' THEN oi.quantity * p.unit_price ELSE 0 END), 2) AS gadgets_revenue,
       ROUND(SUM(CASE WHEN p.category = 'Services' THEN oi.quantity * p.unit_price ELSE 0 END), 2) AS services_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;""",
    },

    # ── Ranking Functions ──
    {
        "id": 10,
        "topic": "Ranking Functions",
        "difficulty": "Medium",
        "title": "ROW_NUMBER – Rank Orders per Customer",
        "question": "For each customer, assign a row number to their orders ordered by date (earliest = 1).",
        "hint": "ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)",
        "answer": """SELECT customer_id, order_id, order_date,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_seq
FROM orders
ORDER BY customer_id, order_seq;""",
    },
    {
        "id": 11,
        "topic": "Ranking Functions",
        "difficulty": "Medium",
        "title": "RANK vs DENSE_RANK – Employee Salary Ranking",
        "question": "Rank employees by salary (highest first). Show RANK() and DENSE_RANK() side by side.",
        "hint": "Two window functions in the same SELECT.",
        "answer": """SELECT employee_id, name, salary,
       RANK() OVER (ORDER BY salary DESC) AS rank_val,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank_val
FROM employees
ORDER BY salary DESC;""",
    },
    {
        "id": 12,
        "topic": "Ranking Functions",
        "difficulty": "Hard",
        "title": "Top-N per Group – Latest Order per Customer",
        "question": "Show only the most recent order for each customer using ROW_NUMBER.",
        "hint": "CTE with ROW_NUMBER, then filter rn = 1.",
        "answer": """WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM orders
)
SELECT customer_id, order_id, order_date, status
FROM ranked
WHERE rn = 1
ORDER BY customer_id;""",
    },

    # ── Value Functions (LAG / LEAD) ──
    {
        "id": 13,
        "topic": "Value Functions",
        "difficulty": "Medium",
        "title": "LAG – Month-over-Month Revenue Change",
        "question": "For customer_id = 1, show monthly revenue alongside previous month's revenue and the change.",
        "hint": "LAG(monthly_revenue) OVER (ORDER BY month)",
        "answer": """SELECT month, monthly_revenue,
       LAG(monthly_revenue) OVER (ORDER BY month) AS prev_month_revenue,
       ROUND(monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month), 2) AS change
FROM monthly_metrics
WHERE customer_id = 1
ORDER BY month;""",
    },
    {
        "id": 14,
        "topic": "Value Functions",
        "difficulty": "Medium",
        "title": "LEAD – Next Order Date",
        "question": "For each order, show the date of the customer's next order using LEAD.",
        "hint": "LEAD(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)",
        "answer": """SELECT customer_id, order_id, order_date,
       LEAD(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_order_date
FROM orders
ORDER BY customer_id, order_date;""",
    },

    # ── Aggregation Windows ──
    {
        "id": 15,
        "topic": "Aggregation Windows",
        "difficulty": "Medium",
        "title": "Running Total – Cumulative Revenue",
        "question": "Show a running total of monthly_revenue for customer_id = 2 ordered by month.",
        "hint": "SUM(monthly_revenue) OVER (ORDER BY month)",
        "answer": """SELECT month, monthly_revenue,
       ROUND(SUM(monthly_revenue) OVER (ORDER BY month), 2) AS cumulative_revenue
FROM monthly_metrics
WHERE customer_id = 2
ORDER BY month;""",
    },
    {
        "id": 16,
        "topic": "Aggregation Windows",
        "difficulty": "Hard",
        "title": "3-Month Moving Average",
        "question": "Calculate a 3-month moving average of monthly_revenue for customer_id = 1.",
        "hint": "AVG(...) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)",
        "answer": """SELECT month, monthly_revenue,
       ROUND(AVG(monthly_revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m
FROM monthly_metrics
WHERE customer_id = 1
ORDER BY month;""",
    },
    {
        "id": 17,
        "topic": "Aggregation Windows",
        "difficulty": "Medium",
        "title": "PARTITION BY – Running Total per Customer",
        "question": "Show running total of monthly_revenue partitioned by customer_id.",
        "hint": "SUM(...) OVER (PARTITION BY customer_id ORDER BY month)",
        "answer": """SELECT customer_id, month, monthly_revenue,
       ROUND(SUM(monthly_revenue) OVER (PARTITION BY customer_id ORDER BY month), 2) AS cumulative_revenue
FROM monthly_metrics
ORDER BY customer_id, month;""",
    },
    {
        "id": 18,
        "topic": "Aggregation Windows",
        "difficulty": "Hard",
        "title": "Advanced Frame – Sum of Previous 2 Months",
        "question": "For customer_id = 3, show the sum of revenue for the previous 2 months only (excluding current).",
        "hint": "ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING",
        "answer": """SELECT month, monthly_revenue,
       SUM(monthly_revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS prev_2m_sum
FROM monthly_metrics
WHERE customer_id = 3
ORDER BY month;""",
    },
    {
        "id": 19,
        "topic": "Aggregation Windows",
        "difficulty": "Hard",
        "title": "Percentile – Median Salary",
        "question": "Find the median (50th percentile) salary from the employees table.",
        "hint": "PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)",
        "answer": """SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
FROM employees;""",
    },

    # ── Mixed / Interview-Style ──
    {
        "id": 20,
        "topic": "Interview Combo",
        "difficulty": "Hard",
        "title": "Revenue Rank per Segment",
        "question": "Rank customers within their segment by total completed-order revenue. Show segment, name, revenue, and rank.",
        "hint": "CTE for revenue, then RANK() OVER (PARTITION BY segment ORDER BY revenue DESC).",
        "answer": """WITH cust_rev AS (
    SELECT c.customer_id, c.name, c.segment,
           ROUND(SUM(oi.quantity * p.unit_price * (1 - COALESCE(o.discount_pct,0)/100.0)),2) AS revenue
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'completed'
    GROUP BY c.customer_id, c.name, c.segment
)
SELECT segment, name, revenue,
       RANK() OVER (PARTITION BY segment ORDER BY revenue DESC) AS segment_rank
FROM cust_rev
ORDER BY segment, segment_rank;""",
    },
    {
        "id": 21,
        "topic": "Interview Combo",
        "difficulty": "Hard",
        "title": "Employee Hierarchy – Manager Chain",
        "question": "Show each employee with their manager's name and their manager's manager's name (2 levels up).",
        "hint": "Double self-join on employees.",
        "answer": """SELECT e.name AS employee,
       m.name AS manager,
       mm.name AS managers_manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
LEFT JOIN employees mm ON m.manager_id = mm.employee_id
ORDER BY e.employee_id;""",
    },
    {
        "id": 22,
        "topic": "Interview Combo",
        "difficulty": "Hard",
        "title": "YoY-style Growth using LAG on Aggregated Data",
        "question": "Show each customer's monthly revenue alongside their previous month's revenue and the percentage change.",
        "hint": "Use LAG partitioned by customer, compute pct change.",
        "answer": """SELECT customer_id, month, monthly_revenue,
       LAG(monthly_revenue) OVER (PARTITION BY customer_id ORDER BY month) AS prev_revenue,
       ROUND(
           (monthly_revenue - LAG(monthly_revenue) OVER (PARTITION BY customer_id ORDER BY month))
           / NULLIF(LAG(monthly_revenue) OVER (PARTITION BY customer_id ORDER BY month), 0) * 100
       , 2) AS pct_change
FROM monthly_metrics
ORDER BY customer_id, month;""",
    },
]

