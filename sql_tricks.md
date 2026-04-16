# 📖 SQL Tricks Booklet
### Your Joyful Guide to Crushing SQL Interviews

> *"SQL is just English for databases. Once you see the patterns, you'll never forget them."*

---

## Table of Contents

1. [🤝 The JOIN Family Reunion](#-the-join-family-reunion)
2. [🧊 The NULL Trap — SQL's Invisible Monster](#-the-null-trap--sqls-invisible-monster)
3. [💰 Revenue Calculations — Follow the Money](#-revenue-calculations--follow-the-money)
4. [📊 GROUP BY & Aggregation — Squish the Data](#-group-by--aggregation--squish-the-data)
5. [🎭 CASE WHEN — SQL's If-Else](#-case-when--sqls-if-else)
6. [🏆 Ranking Functions — Who's #1?](#-ranking-functions--whos-1)
7. [⏮️ LAG & LEAD — Time Travel](#️-lag--lead--time-travel)
8. [📈 Running Totals & Moving Averages](#-running-totals--moving-averages)
9. [🪟 Window Frames — The Secret Sauce](#-window-frames--the-secret-sauce)
10. [🎯 Top-N Queries — The Interview Favorite](#-top-n-queries--the-interview-favorite)
11. [🧩 CTE — Clean Up Your Mess](#-cte--clean-up-your-mess)
12. [⚡ Cheat Sheet — Copy-Paste Gold](#-cheat-sheet--copy-paste-gold)

---

## 🤝 The JOIN Family Reunion

Think of JOINs as a **family reunion**. You have two guest lists (tables) and you need to figure out who shows up together.

### The 4 Types — Visualized

```
Table A (🔵)     Table B (🟡)

   🔵🔵🔵           🟡🟡🟡
     🔵🟡🔵       🟡🔵🟡
       🔵🔵       🟡🟡
```

| JOIN Type | Who Gets Invited | Memory Trick |
|-----------|-----------------|--------------|
| `INNER JOIN` | Only people on BOTH lists | 🤝 "We both know you" |
| `LEFT JOIN` | Everyone from list A + matches from B | 👈 "A always comes, B is optional" |
| `RIGHT JOIN` | Everyone from list B + matches from A | 👉 "B always comes, A is optional" |
| `FULL OUTER JOIN` | EVERYONE from both lists | 🎉 "Nobody gets left out" |

### 🔑 The Golden Rule

```sql
-- LEFT JOIN + WHERE IS NULL = "Who's NOT in the other table?"
SELECT a.*
FROM table_a a
LEFT JOIN table_b b ON a.id = b.a_id
WHERE b.id IS NULL;  -- 👈 This is the magic line
```

**Interview trick:** When they ask *"find customers who never ordered"*, your brain should instantly think: **LEFT JOIN + IS NULL**.

### 🤳 Self-Join — Talking to Yourself

A self-join is when a table joins **itself**. Think of it as an employee org chart:

```sql
-- "Who is my manager?"
SELECT emp.name AS employee, mgr.name AS manager
FROM employees emp
LEFT JOIN employees mgr ON emp.manager_id = mgr.employee_id;
```

**Memory trick:** Same table, TWO aliases. One plays the child, one plays the parent. 👨‍👦

---

## 🧊 The NULL Trap — SQL's Invisible Monster

NULL is NOT zero. NULL is NOT empty string. **NULL is "I don't know."**

### The 3 Rules of NULL

```
Rule 1:  NULL = NULL   → NULL  (not TRUE!)
Rule 2:  NULL + 5      → NULL  (anything + unknown = unknown)
Rule 3:  NULL in WHERE  → row disappears  👻
```

### How to Defend Against NULLs

| Situation | Solution | Example |
|-----------|----------|---------|
| NULL in math | `COALESCE()` | `COALESCE(discount, 0)` |
| NULL in WHERE | `IS NULL` / `IS NOT NULL` | `WHERE city IS NOT NULL` |
| NULL in JOIN | Won't match! | NULLs on both sides ≠ match |
| NULL in aggregation | Ignored by SUM/AVG/COUNT(col) | `COUNT(*)` counts all, `COUNT(col)` skips NULL |

### ⚠️ Interview Trap

```sql
-- This does NOT find NULLs!
SELECT * FROM orders WHERE discount_pct != 10;
-- ❌ Rows where discount_pct IS NULL are EXCLUDED

-- This finds everything except 10:
SELECT * FROM orders WHERE discount_pct != 10 OR discount_pct IS NULL;
-- ✅ Now NULLs are included
```

---

## 💰 Revenue Calculations — Follow the Money

Revenue questions are in **every** SQL interview. Here's the pattern:

```
Revenue = quantity × price × (1 - discount/100)
```

### The Template

```sql
SELECT
    customer_id,
    ROUND(SUM(
        quantity * unit_price * (1 - COALESCE(discount_pct, 0) / 100.0)
    ), 2) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE status = 'completed'        -- 👈 Don't count cancelled orders!
GROUP BY customer_id;
```

### 🎯 Checklist for Revenue Questions

- [ ] Did you handle NULL discounts? → `COALESCE(discount, 0)`
- [ ] Did you filter by status? → `WHERE status = 'completed'`
- [ ] Did you JOIN all needed tables? → orders → order_items → products
- [ ] Did you ROUND the result? → `ROUND(..., 2)`
- [ ] Did you use the right GROUP BY?

---

## 📊 GROUP BY & Aggregation — Squish the Data

**GROUP BY** takes many rows and squishes them into fewer rows.

### Think of it as sorting M&Ms by color:

```
Before:  🔴🔵🔴🟢🔵🔴🟢🔵🔵
After:   🔴 × 3  |  🔵 × 4  |  🟢 × 2
         ↑ GROUP    ↑ COUNT()
```

### The Rule

> Every column in SELECT must be either:
> 1. In the GROUP BY, OR
> 2. Inside an aggregate function (SUM, COUNT, AVG, MAX, MIN)

### HAVING vs WHERE

```
WHERE  → filters BEFORE grouping  (raw rows)
HAVING → filters AFTER grouping   (aggregated results)
```

```sql
-- "Customers who spent more than $500"
SELECT customer_id, SUM(amount) AS total
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 500;    -- 👈 HAVING, not WHERE
```

**Memory trick:** **W**HERE comes first (alphabetically and in execution). **H**AVING comes after **G**ROUP BY.

---

## 🎭 CASE WHEN — SQL's If-Else

CASE turns SQL into a Swiss Army knife. Use it to create new columns based on conditions.

### Pattern 1: Conditional Columns

```sql
SELECT name,
    CASE
        WHEN salary > 100000 THEN '💰 High'
        WHEN salary > 60000  THEN '👍 Mid'
        ELSE '📉 Low'
    END AS salary_band
FROM employees;
```

### Pattern 2: Pivot with CASE (Interview Favorite! ⭐)

```sql
-- Turn categories into columns
SELECT customer_id,
    SUM(CASE WHEN category = 'Widgets'  THEN revenue ELSE 0 END) AS widgets_rev,
    SUM(CASE WHEN category = 'Gadgets'  THEN revenue ELSE 0 END) AS gadgets_rev,
    SUM(CASE WHEN category = 'Services' THEN revenue ELSE 0 END) AS services_rev
FROM sales
GROUP BY customer_id;
```

**Memory trick:** CASE + SUM + GROUP BY = **poor man's PIVOT table** 📊

---

## 🏆 Ranking Functions — Who's #1?

Three ranking functions. They look similar but behave differently with **ties**.

### The Scoreboard Example

| Student | Score | ROW_NUMBER | RANK | DENSE_RANK |
|---------|-------|-----------|------|------------|
| Alice   | 95    | 1         | 1    | 1          |
| Bob     | 95    | 2         | 1    | 1          |
| Charlie | 90    | 3         | **3**| **2**      |
| Diana   | 85    | 4         | 4    | 3          |

### When to use each:

| Function | Ties? | Gaps? | Use When |
|----------|-------|-------|----------|
| `ROW_NUMBER()` | No ties, ever | N/A | Unique row numbering, pagination |
| `RANK()` | Yes, same rank for ties | **Skips numbers** | "Olympic medals" style |
| `DENSE_RANK()` | Yes, same rank for ties | **No gaps** | "Top 3 salary levels" |

### The Template

```sql
SELECT name, salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
    RANK()       OVER (ORDER BY salary DESC) AS rank_val,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank_val
FROM employees;
```

### 🔥 Top-N per Group (THE Interview Question)

```sql
-- "Latest order per customer"
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_date DESC
        ) AS rn
    FROM orders
)
SELECT * FROM ranked WHERE rn = 1;
```

**Memory trick:** CTE + ROW_NUMBER + `WHERE rn = 1` = **Top-1 per group** 🎯

---

## ⏮️ LAG & LEAD — Time Travel

LAG looks **backward**. LEAD looks **forward**. They let you compare a row with its neighbors.

```
         ← LAG (previous)    LEAD (next) →
              ⬅️                ➡️
Row 1:   ...     Jan $100
Row 2:   Jan     Feb $150     Mar
Row 3:   Feb     Mar $120     Apr
Row 4:   Mar     Apr $180     ...
```

### Month-over-Month Change

```sql
SELECT month, revenue,
    LAG(revenue) OVER (ORDER BY month)  AS prev_month,
    revenue - LAG(revenue) OVER (ORDER BY month) AS change
FROM monthly_metrics;
```

### Percentage Change

```sql
SELECT month, revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month))
        / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100
    , 2) AS pct_change
FROM monthly_metrics;
```

**⚠️ Pro tip:** Always wrap the denominator in `NULLIF(..., 0)` to avoid division by zero!

---

## 📈 Running Totals & Moving Averages

### Running Total — The Snowball 🏔️

Each row adds to everything before it:

```
Month   Revenue   Running Total
Jan     $100      $100         ← just Jan
Feb     $150      $250         ← Jan + Feb
Mar     $120      $370         ← Jan + Feb + Mar
```

```sql
SELECT month, revenue,
    SUM(revenue) OVER (ORDER BY month) AS running_total
FROM monthly_metrics;
```

### Moving Average — The Smoothing Iron 🧹

Average of the last N rows (smooths out spikes):

```sql
-- 3-month moving average
SELECT month, revenue,
    AVG(revenue) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3m
FROM monthly_metrics;
```

### With PARTITION BY — Per-Group Calculations

```sql
-- Running total PER customer
SELECT customer_id, month, revenue,
    SUM(revenue) OVER (
        PARTITION BY customer_id    -- 👈 reset for each customer
        ORDER BY month
    ) AS cumulative_revenue
FROM monthly_metrics;
```

---

## 🪟 Window Frames — The Secret Sauce

Window frames control **which rows** the window function looks at.

### The Frame Clause

```sql
ROWS BETWEEN [start] AND [end]
```

| Keyword | Meaning |
|---------|---------|
| `UNBOUNDED PRECEDING` | From the very first row |
| `N PRECEDING` | N rows before current |
| `CURRENT ROW` | This row |
| `N FOLLOWING` | N rows after current |
| `UNBOUNDED FOLLOWING` | To the very last row |

### Visual

```
Row:    1    2    3    [4]    5    6    7

ROWS BETWEEN 2 PRECEDING AND CURRENT ROW:
             [2    3    4]
             ↑ looks at 3 rows

ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING:
                  [3    4    5]
                  ↑ centered window

ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW:
        [1    2    3    4]
        ↑ running total (default!)
```

### Percentiles

```sql
-- Median salary (50th percentile)
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median
FROM employees;
```

---

## 🎯 Top-N Queries — The Interview Favorite

### Simple Top-N

```sql
-- Top 3 customers by revenue
SELECT customer_id, SUM(amount) AS total
FROM orders
GROUP BY customer_id
ORDER BY total DESC
LIMIT 3;
```

### Top-N Per Group (⭐ Most Asked!)

```sql
-- Top 2 products per category
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY revenue DESC
        ) AS rn
    FROM product_sales
)
SELECT * FROM ranked WHERE rn <= 2;
```

---

## 🧩 CTE — Clean Up Your Mess

**CTE (Common Table Expression)** = a temporary named result set. Think of it as a **variable** for SQL.

### Before CTE (messy):

```sql
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (...) AS rn
    FROM (
        SELECT customer_id, SUM(amount) AS total
        FROM orders GROUP BY customer_id
    ) sub
) ranked
WHERE rn <= 3;
```

### After CTE (clean):

```sql
WITH customer_totals AS (
    SELECT customer_id, SUM(amount) AS total
    FROM orders
    GROUP BY customer_id
),
ranked AS (
    SELECT *, ROW_NUMBER() OVER (ORDER BY total DESC) AS rn
    FROM customer_totals
)
SELECT * FROM ranked WHERE rn <= 3;
```

**Memory trick:** CTEs are like **cooking prep** 🍳 — chop your ingredients (data) first, then cook (final SELECT).

---

## ⚡ Cheat Sheet — Copy-Paste Gold

### Window Functions Template

```sql
function_name() OVER (
    [PARTITION BY col1, col2]           -- reset per group
    [ORDER BY col3]                     -- row ordering
    [ROWS BETWEEN start AND end]        -- frame
)
```

### Common Interview Patterns

| Pattern | SQL Skeleton |
|---------|-------------|
| Customers with no orders | `LEFT JOIN ... WHERE b.id IS NULL` |
| Revenue per customer | `SUM(qty * price * (1 - COALESCE(disc,0)/100))` |
| Top-N per group | `CTE + ROW_NUMBER() + WHERE rn <= N` |
| Month-over-month | `LAG(val) OVER (ORDER BY month)` |
| Running total | `SUM(val) OVER (ORDER BY date)` |
| Moving average | `AVG(val) OVER (ROWS BETWEEN N PRECEDING AND CURRENT ROW)` |
| Pivot / Conditional agg | `SUM(CASE WHEN cat='X' THEN val END)` |
| Median | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY col)` |
| Dedup rows | `ROW_NUMBER() OVER (PARTITION BY key ORDER BY ...) = 1` |
| Self-join hierarchy | `LEFT JOIN same_table parent ON child.parent_id = parent.id` |

### Execution Order (How SQL Actually Runs)

```
1. FROM / JOIN     ← tables are loaded
2. WHERE           ← rows filtered
3. GROUP BY        ← rows grouped
4. HAVING          ← groups filtered
5. SELECT          ← columns computed
6. WINDOW          ← window functions run
7. DISTINCT        ← duplicates removed
8. ORDER BY        ← rows sorted
9. LIMIT / OFFSET  ← rows trimmed
```

**This is why you can't use a column alias in WHERE — it hasn't been created yet!** 🤯

---

## 🎓 Final Tips for Interview Day

1. **Always clarify** — "Should I count cancelled orders?" "What about NULLs?"
2. **Start simple** — Get the basic query working, then optimize
3. **Talk through your thinking** — Interviewers care about process, not just the answer
4. **Watch for NULLs** — They're hiding everywhere. Use COALESCE.
5. **CTE over subqueries** — Cleaner, more readable, shows maturity
6. **Test edge cases** — What if a customer has 0 orders? What if there's a tie?

---

<p align="center">
  <b>Now go practice! Open the app and start querying. 🚀</b><br/>
  <code>streamlit run app.py</code>
</p>

