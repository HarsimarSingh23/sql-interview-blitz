import streamlit as st
import streamlit.components.v1 as components
import duckdb
import pandas as pd
import os
from questions import QUESTIONS

# ── Page config ──
st.set_page_config(page_title="Hogwarts School of SQL & Sorcery", page_icon="⚡", layout="wide")

# ── Custom CSS — "Hogwarts" theme + transitions ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=IM+Fell+English:ital@0;1&display=swap');

    /* Candlelit Great Hall backdrop — deep night, warm hearth glow */
    .stApp {
        background:
            radial-gradient(circle at 18% 12%, rgba(211, 166, 37, 0.14), transparent 42%),
            radial-gradient(circle at 82% 16%, rgba(116, 0, 1, 0.28), transparent 46%),
            radial-gradient(circle at 50% 95%, rgba(211, 166, 37, 0.10), transparent 55%),
            #1a1410;
        background-attachment: fixed;
    }

    /* Enchanted golden hero title with candle-flicker glow */
    .arcane-title {
        font-family: 'Cinzel', serif;
        font-size: 2.6em; font-weight: 900; text-align: center;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #b8860b, #f5d67a, #d3a625, #f5d67a, #b8860b);
        background-size: 300% auto;
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 7s linear infinite, flicker 3.5s ease-in-out infinite;
        margin: 0.2em 0;
    }
    @keyframes shimmer { to { background-position: 300% center; } }
    @keyframes flicker {
        0%, 100% { filter: drop-shadow(0 0 8px rgba(211,166,37,0.55)); }
        45%      { filter: drop-shadow(0 0 14px rgba(245,214,122,0.85)); }
        70%      { filter: drop-shadow(0 0 6px rgba(211,166,37,0.40)); }
    }

    .subtitle {
        text-align: center; margin-top: -6px;
        color: #c9a24b; font-family: 'IM Fell English', serif;
        font-style: italic; font-size: 1.1em;
    }

    /* House-banner topic headers — crimson drape with gold trim */
    .topic-header {
        background: linear-gradient(90deg, rgba(116,0,1,0.55), rgba(116,0,1,0.15) 70%, transparent);
        border-left: 4px solid #d3a625;
        padding: 10px 16px; border-radius: 6px; margin: 16px 0 6px 0;
        color: #f5d67a; font-size: 1.2em; font-weight: 700;
        font-family: 'Cinzel', serif; letter-spacing: 0.5px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.35);
        animation: fadeSlide 0.5s ease both;
    }
    @keyframes fadeSlide {
        from { opacity: 0; transform: translateX(-12px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    /* Difficulty = spell-difficulty houses */
    .difficulty-easy   { color: #d3a625; }   /* Hufflepuff gold */
    .difficulty-medium { color: #ecb939; }
    .difficulty-hard   { color: #ae0001; }   /* Gryffindor scarlet */

    /* Expanders: aged-parchment scrolls that lift on hover */
    div[data-testid="stExpander"] {
        border: 1px solid rgba(211,166,37,0.35);
        border-radius: 8px; margin-bottom: 8px;
        background: rgba(40, 30, 20, 0.35);
        backdrop-filter: blur(4px);
        transition: transform 0.2s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }
    div[data-testid="stExpander"]:hover {
        transform: translateY(-2px);
        border-color: rgba(245,214,122,0.75);
        box-shadow: 0 8px 26px rgba(116,0,1,0.35), 0 0 12px rgba(211,166,37,0.25);
    }

    /* Score boxes = house-point hourglasses */
    .score-box {
        background: rgba(40, 30, 20, 0.4);
        border: 1px solid rgba(211,166,37,0.4); border-radius: 10px;
        padding: 16px; text-align: center; margin: 4px;
        transition: transform 0.2s ease, box-shadow 0.25s ease;
    }
    .score-box:hover {
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 6px 22px rgba(211,166,37,0.35);
    }
    .score-number { font-size: 2em; font-weight: 900; font-family: 'Cinzel', serif; }

    /* Buttons: brass-and-crimson with warm hover glow */
    .stButton > button {
        border: 1px solid rgba(211,166,37,0.45);
        color: #f5d67a;
        transition: transform 0.15s ease, box-shadow 0.2s ease, border-color 0.2s ease, background 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: #f5d67a;
        background: rgba(116,0,1,0.35);
        box-shadow: 0 4px 16px rgba(211,166,37,0.4);
    }

    /* Tabs glow gold when active */
    .stTabs [data-baseweb="tab"] { transition: color 0.2s ease; font-family: 'Cinzel', serif; }
    .stTabs [aria-selected="true"] { color: #f5d67a !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #d3a625 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="arcane-title">⚡ Hogwarts School of SQL &amp; Sorcery</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">"It is our queries that show what we truly are, far more than our abilities." — cast wisely.</p>', unsafe_allow_html=True)

# ── Data setup ──
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@st.cache_resource
def get_connection():
    """Create DuckDB in-memory DB and load CSVs as tables."""
    con = duckdb.connect(":memory:")
    for csv_file in ["wizards", "spells", "quests", "quest_casts", "guild", "realm_metrics"]:
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
    tables = ["wizards", "spells", "quests", "quest_casts", "guild", "realm_metrics"]
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
if "house_points" not in st.session_state:
    st.session_state.house_points = 0


# ── 🧙‍♂️ Dumbledore awards points (real browser-side JavaScript) ──
def award_gryffindor(total_points, delta=10):
    """Inject JS that paints a full-page celebration whenever a query succeeds."""
    components.html(f"""
    <script>
    (function() {{
        const delta = {delta}, total = {total_points};
        // Reach into the top Streamlit document so it floats over the WHOLE page,
        // not just this tiny component iframe.
        let doc, root;
        try {{ doc = window.parent.document; root = doc.body; }}
        catch (e) {{ doc = document; root = document.body; }}

        // Inject keyframes once
        if (!doc.getElementById('gp-keyframes')) {{
            const style = doc.createElement('style');
            style.id = 'gp-keyframes';
            style.textContent = `
                @keyframes gpPop  {{ to {{ transform:scale(1); opacity:1; }} }}
                @keyframes gpFall {{
                    0%   {{ opacity:0; transform:translateY(-20px) rotate(0deg); }}
                    12%  {{ opacity:1; }}
                    100% {{ opacity:0; transform:translateY(105vh) rotate(360deg); }}
                }}`;
            doc.head.appendChild(style);
        }}

        const overlay = doc.createElement('div');
        overlay.style.cssText = `position:fixed;inset:0;z-index:999999;pointer-events:none;
            display:flex;align-items:center;justify-content:center;overflow:hidden;
            font-family:'Cinzel',Georgia,serif;`;

        // Golden sparkles raining down
        for (let i = 0; i < 44; i++) {{
            const s = doc.createElement('div');
            const dur = 2.4 + Math.random()*2, delay = Math.random()*0.7;
            s.textContent = Math.random() < 0.5 ? '✨' : '⭐';
            s.style.cssText = `position:absolute;left:${{Math.random()*100}}vw;top:-40px;
                font-size:${{10 + Math.random()*16}}px;opacity:0;
                animation:gpFall ${{dur}}s ease-in ${{delay}}s forwards;`;
            overlay.appendChild(s);
        }}

        // Wax-sealed proclamation card
        const card = doc.createElement('div');
        card.style.cssText = `text-align:center;padding:26px 42px;border-radius:16px;
            background:radial-gradient(circle at 50% 0%, rgba(116,0,1,0.96), rgba(35,10,10,0.97));
            border:2px solid #d3a625;box-shadow:0 0 45px rgba(211,166,37,0.7);
            transform:scale(0.4);opacity:0;animation:gpPop 0.5s cubic-bezier(.2,1.5,.4,1) forwards;`;
        card.innerHTML = `
            <div style="font-size:56px;line-height:1;">🧙‍♂️</div>
            <div style="color:#f5d67a;font-size:27px;font-weight:900;margin-top:8px;letter-spacing:1px;">
                +${{delta}} POINTS TO GRYFFINDOR!</div>
            <div style="color:#e8d8a0;font-size:15px;margin-top:6px;font-style:italic;">
                "Awarded by Prof. Dumbledore for a well-cast query."</div>
            <div style="color:#d3a625;font-size:14px;margin-top:10px;">
                🏆 Gryffindor total: <b>${{total}}</b> points</div>
            <div style="color:#c9a24b;font-size:12px;margin-top:8px;letter-spacing:2px;">
                🎵 ~ Hedwig's Theme ~ 🎵</div>`;
        overlay.appendChild(card);
        root.appendChild(overlay);

        // 🎵 Hedwig's Theme opening motif — synthesized live via WebAudio.
        // (No copyrighted audio is bundled; the notes are generated on the fly.
        //  Silently skipped if the browser blocks autoplay.)
        try {{
            const ac = new (window.AudioContext || window.webkitAudioContext)();
            const beat = 0.30;  // seconds per quarter note — slow 3/4 waltz feel
            // [frequency, duration in beats] — the famous E-minor opening phrase
            const melody = [
                [493.88, 1.0],  // B4
                [659.25, 1.5],  // E5
                [783.99, 0.5],  // G5
                [739.99, 1.0],  // F#5
                [659.25, 2.0],  // E5
                [987.77, 1.0],  // B5
                [880.00, 3.0],  // A5
                [739.99, 3.0],  // F#5
            ];
            let t = ac.currentTime + 0.06;
            for (const [freq, beats] of melody) {{
                const dur = beats * beat;
                // Two detuned voices for a warm, bell-like celesta tone
                [['triangle', 0.11, 0], ['sine', 0.07, 2]].forEach(([type, peak, det]) => {{
                    const o = ac.createOscillator(), g = ac.createGain();
                    o.type = type; o.frequency.value = freq; o.detune.value = det;
                    o.connect(g); g.connect(ac.destination);
                    g.gain.setValueAtTime(0.0001, t);
                    g.gain.exponentialRampToValueAtTime(peak, t + 0.02);
                    g.gain.exponentialRampToValueAtTime(0.0001, t + dur * 0.95);
                    o.start(t); o.stop(t + dur);
                }});
                t += dur;
            }}
        }} catch (e) {{}}

        // Fade out & remove
        setTimeout(() => {{
            card.style.transition = 'opacity 0.6s ease';
            card.style.opacity = '0';
            setTimeout(() => overlay.remove(), 700);
        }}, 4200);
    }})();
    </script>
    """, height=0)

# ── Sidebar ──
with st.sidebar:
    st.title("⚡ Hogwarts SQL")
    st.markdown("**School of SQL & Sorcery**")

    # 🏆 Gryffindor house-points hourglass
    st.markdown(
        f'''<div class="score-box" style="border-color:#ae0001;background:rgba(116,0,1,0.28);margin-top:10px;">
        <div style="font-size:0.8em;color:#d3a625;letter-spacing:2px;">🏆 GRYFFINDOR</div>
        <div class="score-number" style="color:#f5d67a;">{st.session_state.house_points}</div>
        <div style="font-size:0.75em;color:#c9a24b;">house points</div></div>''',
        unsafe_allow_html=True,
    )
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
    for t in ["wizards", "spells", "quests", "quest_casts", "guild", "realm_metrics"]:
        st.code(t, language="text")

    if st.button("🔄 Reset Progress", use_container_width=True):
        st.session_state.score = {}
        st.session_state.show_answer = set()
        st.session_state.house_points = 0
        st.rerun()

# ── Main Area ──
tab1, tab2, tab3, tab4 = st.tabs(["📝 Questions", "🔍 Free SQL Editor", "📊 Data Explorer", "📖 SQL Tricks Booklet"])

# ═══════════════════════ TAB 1: Questions ═══════════════════════
with tab1:
    st.header("📜 Spellbook Challenges")

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
                            if st.session_state.score.get(qid) != "solved":
                                st.session_state.score[qid] = "attempted"
                            # 🧙‍♂️ A successful cast earns Gryffindor 10 points
                            st.session_state.house_points += 10
                            award_gryffindor(st.session_state.house_points)
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
                             placeholder="SELECT * FROM wizards LIMIT 5;")
    
    if st.button("▶️ Execute", key="free_run", use_container_width=True):
        if free_sql.strip():
            try:
                result = con.execute(free_sql).fetchdf()
                st.success(f"✅ {len(result)} rows returned")
                st.dataframe(result, use_container_width=True)
                # 🧙‍♂️ A successful cast earns Gryffindor 10 points
                st.session_state.house_points += 10
                award_gryffindor(st.session_state.house_points)
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

    tables = ["wizards", "spells", "quests", "quest_casts", "guild", "realm_metrics"]
    
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

