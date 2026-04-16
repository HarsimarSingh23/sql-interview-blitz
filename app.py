import streamlit as st
import duckdb
import pandas as pd
import os
from questions import QUESTIONS

# ── Page config ──
st.set_page_config(page_title="SQL Interview Practice", page_icon="🧑‍💻", layout="wide")

# ── Custom CSS ──
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .topic-header { 
        background: linear-gradient(90deg, #1e3a5f, #0e1117);
        padding: 8px 16px; border-radius: 8px; margin: 8px 0;
        color: #58a6ff; font-size: 1.1em; font-weight: 600;
    }
    .difficulty-easy { color: #3fb950; }
    .difficulty-medium { color: #d29922; }
    .difficulty-hard { color: #f85149; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; border-radius: 8px; margin-bottom: 4px; }
    .score-box {
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 16px; text-align: center; margin: 4px;
    }
    .score-number { font-size: 2em; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── Data setup ──
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@st.cache_resource
def get_connection():
    """Create DuckDB in-memory DB and load CSVs as tables."""
    con = duckdb.connect(":memory:")
    for csv_file in ["customers", "products", "orders", "order_items", "employees", "monthly_metrics"]:
        path = os.path.join(DATA_DIR, f"{csv_file}.csv")
        if os.path.exists(path):
            con.execute(f"CREATE TABLE {csv_file} AS SELECT * FROM read_csv_auto('{path}')")
    return con

con = get_connection()

# ── Helper: Show table previews ──
def show_table_previews():
    """Render expandable table previews."""
    st.markdown("---")
    st.subheader("📊 Quick Table Reference")
    tables = ["customers", "products", "orders", "order_items", "employees", "monthly_metrics"]
    cols = st.columns(3)
    for i, table in enumerate(tables):
        with cols[i % 3]:
            with st.expander(f"🗂️ {table}"):
                try:
                    df = con.execute(f"SELECT * FROM {table}").fetchdf()
                    st.caption(f"{len(df)} rows × {len(df.columns)} cols")
                    st.dataframe(df, use_container_width=True, height=250)
                except Exception as e:
                    st.error(str(e))

# ── Session state ──
if "score" not in st.session_state:
    st.session_state.score = {}
if "show_answer" not in st.session_state:
    st.session_state.show_answer = set()

# ── Sidebar ──
with st.sidebar:
    st.title("🧑‍💻 SQL Practice Tool")
    st.markdown("**Self-practice for SQL interviews**")
    st.divider()

    # Score summary
    total = len(QUESTIONS)
    solved = sum(1 for v in st.session_state.score.values() if v == "solved")
    attempted = len(st.session_state.score)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="score-box"><div class="score-number" style="color:#3fb950">{solved}</div>Solved</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="score-box"><div class="score-number" style="color:#d29922">{attempted - solved}</div>Attempted</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="score-box"><div class="score-number" style="color:#58a6ff">{total}</div>Total</div>', unsafe_allow_html=True)

    st.divider()
    
    # Filters
    topics = sorted(set(q["topic"] for q in QUESTIONS))
    selected_topic = st.selectbox("📂 Filter by Topic", ["All"] + topics)
    selected_diff = st.selectbox("🎯 Filter by Difficulty", ["All", "Easy", "Medium", "Hard"])

    st.divider()
    st.markdown("### 📊 Tables Available")
    for t in ["customers", "products", "orders", "order_items", "employees", "monthly_metrics"]:
        st.code(t, language="text")

    if st.button("🔄 Reset Progress", use_container_width=True):
        st.session_state.score = {}
        st.session_state.show_answer = set()
        st.rerun()

# ── Main Area ──
tab1, tab2, tab3, tab4 = st.tabs(["📝 Questions", "🔍 Free SQL Editor", "📊 Data Explorer", "📖 SQL Tricks Booklet"])

# ═══════════════════════ TAB 1: Questions ═══════════════════════
with tab1:
    st.header("SQL Interview Questions")

    # Show/hide table data
    if st.toggle("👀 Show Table Data", key="show_tables_q", value=False):
        show_table_previews()
        st.markdown("---")

    filtered = QUESTIONS
    if selected_topic != "All":
        filtered = [q for q in filtered if q["topic"] == selected_topic]
    if selected_diff != "All":
        filtered = [q for q in filtered if q["difficulty"] == selected_diff]

    if not filtered:
        st.info("No questions match your filters.")
    
    current_topic = None
    for q in filtered:
        # Topic header
        if q["topic"] != current_topic:
            current_topic = q["topic"]
            st.markdown(f'<div class="topic-header">📁 {current_topic}</div>', unsafe_allow_html=True)

        qid = q["id"]
        diff_class = f"difficulty-{q['difficulty'].lower()}"
        status_icon = "✅" if st.session_state.score.get(qid) == "solved" else "⬜"
        
        with st.expander(f"{status_icon} Q{qid}. {q['title']}  — `{q['difficulty']}`"):
            st.markdown(f"**{q['question']}**")
            
            # Hint toggle
            if st.checkbox(f"💡 Show Hint", key=f"hint_{qid}"):
                st.info(q["hint"])

            # SQL Editor
            user_sql = st.text_area("Write your SQL:", height=150, key=f"sql_{qid}",
                                     placeholder="SELECT ... FROM ...")

            col_run, col_answer = st.columns([1, 1])
            
            with col_run:
                if st.button("▶️ Run Query", key=f"run_{qid}", use_container_width=True):
                    if user_sql.strip():
                        try:
                            result = con.execute(user_sql).fetchdf()
                            st.dataframe(result, use_container_width=True)
                            st.session_state.score[qid] = st.session_state.score.get(qid, "attempted")
                            if st.session_state.score[qid] != "solved":
                                st.session_state.score[qid] = "attempted"
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                    else:
                        st.warning("Write a query first!")

            with col_answer:
                if st.button("👁️ Show Answer", key=f"ans_btn_{qid}", use_container_width=True):
                    st.session_state.show_answer.add(qid)
            
            if qid in st.session_state.show_answer:
                st.markdown("**✅ Reference Answer:**")
                st.code(q["answer"], language="sql")
                # Run reference answer
                try:
                    ref_result = con.execute(q["answer"]).fetchdf()
                    st.dataframe(ref_result, use_container_width=True, height=200)
                except Exception as e:
                    st.error(f"Error in reference: {e}")

            # Mark as solved
            if st.button("✅ Mark as Solved", key=f"solve_{qid}", use_container_width=True):
                st.session_state.score[qid] = "solved"
                st.rerun()


# ═══════════════════════ TAB 2: Free Editor ═══════════════════════
with tab2:
    st.header("🔍 Free SQL Editor")
    st.markdown("Run any SQL query against the loaded tables.")

    # Show/hide table data
    if st.toggle("👀 Show Table Data", key="show_tables_editor", value=False):
        show_table_previews()
        st.markdown("---")

    free_sql = st.text_area("SQL Query:", height=200, key="free_sql",
                             placeholder="SELECT * FROM customers LIMIT 5;")
    
    if st.button("▶️ Execute", key="free_run", use_container_width=True):
        if free_sql.strip():
            try:
                result = con.execute(free_sql).fetchdf()
                st.success(f"✅ {len(result)} rows returned")
                st.dataframe(result, use_container_width=True)
            except Exception as e:
                st.error(f"❌ {e}")
        else:
            st.warning("Enter a query first.")

    # Quick reference
    with st.expander("📖 Quick SQL Reference"):
        st.markdown("""
| Function | Syntax |
|----------|--------|
| `ROW_NUMBER()` | `ROW_NUMBER() OVER (PARTITION BY col ORDER BY col)` |
| `RANK()` | `RANK() OVER (ORDER BY col DESC)` |
| `DENSE_RANK()` | `DENSE_RANK() OVER (ORDER BY col DESC)` |
| `LAG()` | `LAG(col, 1) OVER (ORDER BY col)` |
| `LEAD()` | `LEAD(col, 1) OVER (ORDER BY col)` |
| `Running Sum` | `SUM(col) OVER (ORDER BY col)` |
| `Moving Avg` | `AVG(col) OVER (ORDER BY col ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` |
| `PERCENTILE` | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY col)` |
| `COALESCE` | `COALESCE(col, 0)` |
| `CASE` | `CASE WHEN cond THEN val ELSE val2 END` |
        """)


# ═══════════════════════ TAB 3: Data Explorer ═══════════════════════
with tab3:
    st.header("📊 Data Explorer")
    st.markdown("Browse all available tables and their schemas.")

    tables = ["customers", "products", "orders", "order_items", "employees", "monthly_metrics"]
    
    for table in tables:
        with st.expander(f"📋 {table}"):
            try:
                df = con.execute(f"SELECT * FROM {table}").fetchdf()
                
                # Schema
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("**Schema:**")
                    schema = con.execute(f"DESCRIBE {table}").fetchdf()
                    st.dataframe(schema, use_container_width=True, height=200)
                with col2:
                    st.markdown(f"**Data ({len(df)} rows):**")
                    st.dataframe(df, use_container_width=True, height=300)
            except Exception as e:
                st.error(f"Error: {e}")


# ═══════════════════════ TAB 4: SQL Tricks Booklet ═══════════════════════
with tab4:
    booklet_path = os.path.join(os.path.dirname(__file__), "sql_tricks.md")
    if os.path.exists(booklet_path):
        with open(booklet_path, "r") as f:
            st.markdown(f.read(), unsafe_allow_html=True)
    else:
        st.warning("sql_tricks.md not found. Run generate_data.py first.")

