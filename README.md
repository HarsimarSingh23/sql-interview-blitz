# 🧑‍💻 SQL Interview Blitz — Practice SQL Like a Pro

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.45+-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/DuckDB-In--Browser_SQL-FFC107?logo=duckdb&logoColor=black" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
  <img src="https://img.shields.io/github/stars/HarsimarSingh23/sql-interview-blitz?style=social" />
</p>

<p align="center">
  <b>A self-practice SQL tool that runs entirely in your browser.<br/>No database setup. No cloud accounts. Just you and SQL. 🚀</b>
</p>

---

## 🎯 What Is This?

**SQL Interview Blitz** is an interactive, offline-first SQL practice environment built with Streamlit + DuckDB. It loads realistic CSV datasets into an in-memory database so you can write and run real SQL queries — right in your browser.

Perfect for:
- 🎓 **Students** preparing for database exams
- 💼 **Job seekers** grinding SQL interview rounds
- 🧪 **Anyone** who wants to sharpen SQL without spinning up Postgres

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📝 **22 Curated Questions** | Covers JOINs, aggregation, window functions, CTEs, and more |
| 🖥️ **In-Browser SQL Editor** | Write & run queries instantly — powered by DuckDB |
| 📊 **6 Realistic Tables** | Customers, Products, Orders, Employees, Monthly Metrics |
| 💡 **Hints & Answers** | Toggle hints, reveal reference answers with output |
| 🏆 **Progress Tracker** | Mark questions solved, filter by topic/difficulty |
| 🔍 **Free SQL Sandbox** | Open editor to experiment with any query |
| 📖 **SQL Tricks Booklet** | Built-in cheat sheet with visual explanations |
| 🌙 **Dark Theme** | Easy on the eyes during late-night grinding |

---

## 🗂️ Topics Covered

```
┌─────────────────────────────────────────────────┐
│  JOIN Edge Cases          │  NULLs, Self-Join,  │
│                           │  FULL OUTER JOIN     │
├───────────────────────────┼──────────────────────┤
│  Revenue Calculations     │  Multi-table JOINs,  │
│                           │  COALESCE, discounts │
├───────────────────────────┼──────────────────────┤
│  Aggregation              │  GROUP BY, HAVING,   │
│                           │  Top-N, CASE WHEN    │
├───────────────────────────┼──────────────────────┤
│  Ranking Functions        │  ROW_NUMBER, RANK,   │
│                           │  DENSE_RANK          │
├───────────────────────────┼──────────────────────┤
│  Value Functions          │  LAG, LEAD           │
├───────────────────────────┼──────────────────────┤
│  Window Aggregations      │  Running total,      │
│                           │  Moving average,     │
│                           │  PARTITION BY,       │
│                           │  ROWS BETWEEN,       │
│                           │  PERCENTILE_CONT     │
├───────────────────────────┼──────────────────────┤
│  Interview Combos         │  Mixed real-world    │
│                           │  scenarios           │
└───────────────────────────┴──────────────────────┘
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/HarsimarSingh23/sql-interview-blitz.git
cd sql-interview-blitz

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the CSV data
python generate_data.py

# 4. Launch the app
streamlit run app.py
```

Open **http://localhost:8501** and start practicing! 🎉

---

## 📸 Screenshots

### Questions Tab
> Write SQL, run it, get instant results. Toggle hints and reference answers.

### Free SQL Editor
> Open sandbox to test any query. Built-in syntax reference card.

### Data Explorer
> Browse schemas and data for all 6 tables before writing queries.

---

## 📁 Project Structure

```
sql-interview-blitz/
├── app.py              # Main Streamlit application
├── questions.py        # 22 curated SQL questions with answers
├── generate_data.py    # Script to generate CSV datasets
├── sql_tricks.md       # 📖 SQL Tricks Booklet (read it!)
├── requirements.txt    # Python dependencies
├── data/               # Generated CSV files
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── employees.csv
│   └── monthly_metrics.csv
└── README.md
```

---

## 🧠 The SQL Tricks Booklet

We included a **[SQL Tricks Booklet](sql_tricks.md)** — a fun, visual guide to every concept tested in this tool. It's written to be joyful and memorable, not boring textbook stuff.

Topics include:
- 🤝 The JOIN Family Reunion
- 🧊 The NULL Trap
- 🪟 Window Functions Explained with Emojis
- 🏆 Ranking — Who's #1?
- ⏮️ Time Travel with LAG & LEAD
- 📈 Running Totals & Moving Averages
- And more...

**[→ Read the Booklet](sql_tricks.md)**

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io/) | Web UI framework |
| [DuckDB](https://duckdb.org/) | In-process SQL engine (no server needed) |
| [Pandas](https://pandas.pydata.org/) | Data handling |
| Python 3.9+ | Runtime |

---

## 🤝 Contributing

Found a bug? Want to add questions? PRs are welcome!

1. Fork the repo
2. Create your branch (`git checkout -b feature/new-questions`)
3. Commit changes (`git commit -m 'Add 5 new CTE questions'`)
4. Push & open a PR

---

## ⭐ Star This Repo

If this helped you prep for interviews, smash that ⭐ button! It helps others find this tool.

---

## 📜 License

MIT License — use it, share it, learn from it.

---

<p align="center">
  Made with ❤️ for SQL interview grinders everywhere.<br/>
  <b>Stop reading. Start querying. 🚀</b>
</p>

