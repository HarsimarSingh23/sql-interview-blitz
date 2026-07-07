# 🧙 SQL Spellforge Academy — question bank
# Gold earned on a quest = times_cast × mana_cost × (1 - guild_cut_pct/100)

QUESTIONS = [
    # ═══════════════ JOIN Edge Cases ═══════════════
    {
        "id": 1,
        "topic": "JOIN Edge Cases",
        "difficulty": "Easy",
        "title": "Inner Join – Wizards on Quests",
        "question": "List every wizard who has undertaken at least one quest. Show wizard_id, name, and quest_id.",
        "hint": "INNER JOIN wizards and quests.",
        "answer": """SELECT w.wizard_id, w.name, q.quest_id
FROM wizards w
INNER JOIN quests q ON w.wizard_id = q.wizard_id
ORDER BY w.wizard_id, q.quest_id;""",
    },
    {
        "id": 2,
        "topic": "JOIN Edge Cases",
        "difficulty": "Easy",
        "title": "Left Join – Idle Wizards",
        "question": "Find wizards who have NEVER undertaken a quest. Show wizard_id and name.",
        "hint": "LEFT JOIN + WHERE quest_id IS NULL.",
        "answer": """SELECT w.wizard_id, w.name
FROM wizards w
LEFT JOIN quests q ON w.wizard_id = q.wizard_id
WHERE q.quest_id IS NULL;""",
    },
    {
        "id": 3,
        "topic": "JOIN Edge Cases",
        "difficulty": "Medium",
        "title": "Self Join – Who Mentors Whom",
        "question": "Show each wizard and the name of their mentor. Include self-taught wizards (show NULL for mentor).",
        "hint": "Self LEFT JOIN on wizards using mentor_id.",
        "answer": """SELECT w.wizard_id, w.name, m.name AS mentor_name
FROM wizards w
LEFT JOIN wizards m ON w.mentor_id = m.wizard_id
ORDER BY w.wizard_id;""",
    },
    {
        "id": 4,
        "topic": "JOIN Edge Cases",
        "difficulty": "Medium",
        "title": "NULLs in Joins – Uncharted Quests",
        "question": "List quests where guild_cut_pct IS NULL. Show quest_id, wizard name, and guild_cut_pct.",
        "hint": "JOIN quests and wizards, filter WHERE guild_cut_pct IS NULL.",
        "answer": """SELECT q.quest_id, w.name, q.guild_cut_pct
FROM quests q
JOIN wizards w ON q.wizard_id = w.wizard_id
WHERE q.guild_cut_pct IS NULL;""",
    },
    {
        "id": 5,
        "topic": "JOIN Edge Cases",
        "difficulty": "Hard",
        "title": "Full Outer Join",
        "question": "Show ALL wizards and ALL quests, even where they don't match, using a FULL OUTER JOIN.",
        "hint": "DuckDB supports FULL OUTER JOIN directly.",
        "answer": """SELECT w.wizard_id, w.name, q.quest_id, q.quest_date
FROM wizards w
FULL OUTER JOIN quests q ON w.wizard_id = q.wizard_id
ORDER BY w.wizard_id, q.quest_id;""",
    },
    {
        "id": 6,
        "topic": "JOIN Edge Cases",
        "difficulty": "Medium",
        "title": "Cross Join – Spell Matchups",
        "question": "Generate every possible pairing of two DIFFERENT spells (no spell paired with itself, no duplicate reversed pairs).",
        "hint": "CROSS JOIN spells to itself, then keep pairs where a.spell_id < b.spell_id.",
        "answer": """SELECT a.spell_name AS spell_a, b.spell_name AS spell_b
FROM spells a
JOIN spells b ON a.spell_id < b.spell_id
ORDER BY a.spell_name, b.spell_name;""",
    },

    # ═══════════════ Gold & Aggregation ═══════════════
    {
        "id": 7,
        "topic": "Gold & Aggregation",
        "difficulty": "Medium",
        "title": "Gold Earned per Quest",
        "question": "Compute total gold earned per completed quest: times_cast × mana_cost × (1 - guild_cut_pct/100). Treat NULL guild_cut as 0.",
        "hint": "JOIN quests, quest_casts, spells. COALESCE the cut.",
        "answer": """SELECT q.quest_id,
       ROUND(SUM(qc.times_cast * s.mana_cost * (1 - COALESCE(q.guild_cut_pct, 0) / 100.0)), 2) AS gold_earned
FROM quests q
JOIN quest_casts qc ON q.quest_id = qc.quest_id
JOIN spells s ON qc.spell_id = s.spell_id
WHERE q.status = 'completed'
GROUP BY q.quest_id
ORDER BY gold_earned DESC;""",
    },
    {
        "id": 8,
        "topic": "Gold & Aggregation",
        "difficulty": "Medium",
        "title": "Wizard-Level Aggregation",
        "question": "For each wizard, show total quests, total gold, and average gold per quest — completed quests only.",
        "hint": "Group by wizard after joining all tables.",
        "answer": """SELECT w.wizard_id, w.name,
       COUNT(DISTINCT q.quest_id) AS total_quests,
       ROUND(SUM(qc.times_cast * s.mana_cost * (1 - COALESCE(q.guild_cut_pct, 0) / 100.0)), 2) AS total_gold,
       ROUND(SUM(qc.times_cast * s.mana_cost * (1 - COALESCE(q.guild_cut_pct, 0) / 100.0)) / COUNT(DISTINCT q.quest_id), 2) AS avg_gold_per_quest
FROM wizards w
JOIN quests q ON w.wizard_id = q.wizard_id
JOIN quest_casts qc ON q.quest_id = qc.quest_id
JOIN spells s ON qc.spell_id = s.spell_id
WHERE q.status = 'completed'
GROUP BY w.wizard_id, w.name
ORDER BY total_gold DESC;""",
    },
    {
        "id": 9,
        "topic": "Gold & Aggregation",
        "difficulty": "Medium",
        "title": "Top-3 Wizards by Gold",
        "question": "Show the top 3 wizards by total gold from completed quests.",
        "hint": "Aggregate gold per wizard, then LIMIT 3.",
        "answer": """SELECT w.wizard_id, w.name,
       ROUND(SUM(qc.times_cast * s.mana_cost * (1 - COALESCE(q.guild_cut_pct, 0) / 100.0)), 2) AS total_gold
FROM wizards w
JOIN quests q ON w.wizard_id = q.wizard_id
JOIN quest_casts qc ON q.quest_id = qc.quest_id
JOIN spells s ON qc.spell_id = s.spell_id
WHERE q.status = 'completed'
GROUP BY w.wizard_id, w.name
ORDER BY total_gold DESC
LIMIT 3;""",
    },
    {
        "id": 10,
        "topic": "Gold & Aggregation",
        "difficulty": "Medium",
        "title": "Conditional Aggregation – Gold by School",
        "question": "Per wizard, pivot gold earned by spell school into columns: pyromancy_gold, cryomancy_gold, arcane_gold.",
        "hint": "SUM(CASE WHEN school = '...' THEN ... END).",
        "answer": """SELECT w.wizard_id, w.name,
       ROUND(SUM(CASE WHEN s.school = 'Pyromancy' THEN qc.times_cast * s.mana_cost ELSE 0 END), 2) AS pyromancy_gold,
       ROUND(SUM(CASE WHEN s.school = 'Cryomancy' THEN qc.times_cast * s.mana_cost ELSE 0 END), 2) AS cryomancy_gold,
       ROUND(SUM(CASE WHEN s.school = 'Arcane'    THEN qc.times_cast * s.mana_cost ELSE 0 END), 2) AS arcane_gold
FROM wizards w
JOIN quests q ON w.wizard_id = q.wizard_id
JOIN quest_casts qc ON q.quest_id = qc.quest_id
JOIN spells s ON qc.spell_id = s.spell_id
WHERE q.status = 'completed'
GROUP BY w.wizard_id, w.name
ORDER BY w.wizard_id;""",
    },
    {
        "id": 11,
        "topic": "Gold & Aggregation",
        "difficulty": "Medium",
        "title": "HAVING – Prolific Wizards",
        "question": "List wizards who have completed MORE than 2 quests. Show name and completed-quest count.",
        "hint": "GROUP BY then filter with HAVING COUNT(...) > 2.",
        "answer": """SELECT w.name, COUNT(*) AS completed_quests
FROM wizards w
JOIN quests q ON w.wizard_id = q.wizard_id
WHERE q.status = 'completed'
GROUP BY w.name
HAVING COUNT(*) > 2
ORDER BY completed_quests DESC;""",
    },

    # ═══════════════ Ranking Functions ═══════════════
    {
        "id": 12,
        "topic": "Ranking Functions",
        "difficulty": "Medium",
        "title": "ROW_NUMBER – Quest Sequence per Wizard",
        "question": "For each wizard, number their quests by date (earliest = 1).",
        "hint": "ROW_NUMBER() OVER (PARTITION BY wizard_id ORDER BY quest_date).",
        "answer": """SELECT wizard_id, quest_id, quest_date,
       ROW_NUMBER() OVER (PARTITION BY wizard_id ORDER BY quest_date) AS quest_seq
FROM quests
ORDER BY wizard_id, quest_seq;""",
    },
    {
        "id": 13,
        "topic": "Ranking Functions",
        "difficulty": "Medium",
        "title": "RANK vs DENSE_RANK – Guild Power",
        "question": "Rank guild members by power_level (highest first). Show RANK() and DENSE_RANK() side by side. (Two members are tied!)",
        "hint": "Two window functions in one SELECT reveals the tie behavior.",
        "answer": """SELECT member_id, name, power_level,
       RANK() OVER (ORDER BY power_level DESC) AS rank_val,
       DENSE_RANK() OVER (ORDER BY power_level DESC) AS dense_rank_val
FROM guild
ORDER BY power_level DESC;""",
    },
    {
        "id": 14,
        "topic": "Ranking Functions",
        "difficulty": "Hard",
        "title": "Top-N per Group – Latest Quest per Wizard",
        "question": "Show only the most recent quest for each wizard using ROW_NUMBER.",
        "hint": "CTE with ROW_NUMBER, filter rn = 1.",
        "answer": """WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY wizard_id ORDER BY quest_date DESC) AS rn
    FROM quests
)
SELECT wizard_id, quest_id, quest_date, status
FROM ranked
WHERE rn = 1
ORDER BY wizard_id;""",
    },
    {
        "id": 15,
        "topic": "Ranking Functions",
        "difficulty": "Hard",
        "title": "NTILE – Quartiles of Guild Power",
        "question": "Split guild members into 4 power quartiles (1 = strongest). Show name, power_level, and quartile.",
        "hint": "NTILE(4) OVER (ORDER BY power_level DESC).",
        "answer": """SELECT name, power_level,
       NTILE(4) OVER (ORDER BY power_level DESC) AS power_quartile
FROM guild
ORDER BY power_level DESC;""",
    },

    # ═══════════════ Value Functions (LAG / LEAD) ═══════════════
    {
        "id": 16,
        "topic": "Value Functions",
        "difficulty": "Medium",
        "title": "LAG – Month-over-Month Gold Change",
        "question": "For wizard_id = 1, show monthly gold alongside the previous month's gold and the change.",
        "hint": "LAG(gold_earned) OVER (ORDER BY month).",
        "answer": """SELECT month, gold_earned,
       LAG(gold_earned) OVER (ORDER BY month) AS prev_month_gold,
       ROUND(gold_earned - LAG(gold_earned) OVER (ORDER BY month), 2) AS change
FROM realm_metrics
WHERE wizard_id = 1
ORDER BY month;""",
    },
    {
        "id": 17,
        "topic": "Value Functions",
        "difficulty": "Medium",
        "title": "LEAD – Days Until Next Quest",
        "question": "For each quest, show the date of the wizard's next quest using LEAD.",
        "hint": "LEAD(quest_date) OVER (PARTITION BY wizard_id ORDER BY quest_date).",
        "answer": """SELECT wizard_id, quest_id, quest_date,
       LEAD(quest_date) OVER (PARTITION BY wizard_id ORDER BY quest_date) AS next_quest_date
FROM quests
ORDER BY wizard_id, quest_date;""",
    },
    {
        "id": 18,
        "topic": "Value Functions",
        "difficulty": "Hard",
        "title": "FIRST_VALUE – Gap From Best Month",
        "question": "For wizard_id = 2, show each month's gold and how far below the wizard's single best month it is.",
        "hint": "FIRST_VALUE(gold_earned) OVER (ORDER BY gold_earned DESC ...) with a full frame.",
        "answer": """SELECT month, gold_earned,
       ROUND(FIRST_VALUE(gold_earned) OVER (
           ORDER BY gold_earned DESC
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) - gold_earned, 2) AS gap_from_best
FROM realm_metrics
WHERE wizard_id = 2
ORDER BY month;""",
    },

    # ═══════════════ Aggregation Windows ═══════════════
    {
        "id": 19,
        "topic": "Aggregation Windows",
        "difficulty": "Medium",
        "title": "Running Total – Cumulative Gold",
        "question": "Show a running total of gold_earned for wizard_id = 2 ordered by month.",
        "hint": "SUM(gold_earned) OVER (ORDER BY month).",
        "answer": """SELECT month, gold_earned,
       ROUND(SUM(gold_earned) OVER (ORDER BY month), 2) AS cumulative_gold
FROM realm_metrics
WHERE wizard_id = 2
ORDER BY month;""",
    },
    {
        "id": 20,
        "topic": "Aggregation Windows",
        "difficulty": "Hard",
        "title": "3-Month Moving Average",
        "question": "Calculate a 3-month moving average of gold_earned for wizard_id = 1.",
        "hint": "AVG(...) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW).",
        "answer": """SELECT month, gold_earned,
       ROUND(AVG(gold_earned) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m
FROM realm_metrics
WHERE wizard_id = 1
ORDER BY month;""",
    },
    {
        "id": 21,
        "topic": "Aggregation Windows",
        "difficulty": "Medium",
        "title": "PARTITION BY – Running Total per Wizard",
        "question": "Show a running total of gold_earned partitioned by wizard_id.",
        "hint": "SUM(...) OVER (PARTITION BY wizard_id ORDER BY month).",
        "answer": """SELECT wizard_id, month, gold_earned,
       ROUND(SUM(gold_earned) OVER (PARTITION BY wizard_id ORDER BY month), 2) AS cumulative_gold
FROM realm_metrics
ORDER BY wizard_id, month;""",
    },
    {
        "id": 22,
        "topic": "Aggregation Windows",
        "difficulty": "Hard",
        "title": "Advanced Frame – Sum of Previous 2 Months",
        "question": "For wizard_id = 3, show the sum of gold for the previous 2 months only (excluding the current month).",
        "hint": "ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING.",
        "answer": """SELECT month, gold_earned,
       SUM(gold_earned) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING) AS prev_2m_sum
FROM realm_metrics
WHERE wizard_id = 3
ORDER BY month;""",
    },
    {
        "id": 23,
        "topic": "Aggregation Windows",
        "difficulty": "Hard",
        "title": "Percentile – Median Power Level",
        "question": "Find the median (50th percentile) power_level of the guild.",
        "hint": "PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY power_level).",
        "answer": """SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY power_level) AS median_power
FROM guild;""",
    },
    {
        "id": 24,
        "topic": "Aggregation Windows",
        "difficulty": "Hard",
        "title": "Share of Total – Gold % per Wizard-Month",
        "question": "For each realm_metrics row, show what percent of that wizard's YEARLY gold the month represents.",
        "hint": "gold_earned / SUM(gold_earned) OVER (PARTITION BY wizard_id) * 100.",
        "answer": """SELECT wizard_id, month, gold_earned,
       ROUND(gold_earned / SUM(gold_earned) OVER (PARTITION BY wizard_id) * 100, 2) AS pct_of_year
FROM realm_metrics
ORDER BY wizard_id, month;""",
    },

    # ═══════════════ Subqueries & CTEs ═══════════════
    {
        "id": 25,
        "topic": "Subqueries & CTEs",
        "difficulty": "Medium",
        "title": "Scalar Subquery – Above-Average Mana",
        "question": "List spells whose mana_cost is above the average mana_cost of all spells.",
        "hint": "WHERE mana_cost > (SELECT AVG(mana_cost) FROM spells).",
        "answer": """SELECT spell_name, mana_cost
FROM spells
WHERE mana_cost > (SELECT AVG(mana_cost) FROM spells)
ORDER BY mana_cost DESC;""",
    },
    {
        "id": 26,
        "topic": "Subqueries & CTEs",
        "difficulty": "Medium",
        "title": "EXISTS – Wizards Who Cast Necromancy",
        "question": "Find wizards who have cast at least one Necromancy spell on any quest.",
        "hint": "Correlated EXISTS across quests → quest_casts → spells.",
        "answer": """SELECT DISTINCT w.wizard_id, w.name
FROM wizards w
WHERE EXISTS (
    SELECT 1
    FROM quests q
    JOIN quest_casts qc ON q.quest_id = qc.quest_id
    JOIN spells s ON qc.spell_id = s.spell_id
    WHERE q.wizard_id = w.wizard_id AND s.school = 'Necromancy'
)
ORDER BY w.wizard_id;""",
    },
    {
        "id": 27,
        "topic": "Subqueries & CTEs",
        "difficulty": "Hard",
        "title": "Correlated Subquery – Most-Cast Spell per Wizard",
        "question": "For each wizard, find their single most-cast spell (by total times_cast). Show wizard name, spell name, total casts.",
        "hint": "CTE of totals + ROW_NUMBER per wizard, keep rn = 1.",
        "answer": """WITH casts AS (
    SELECT q.wizard_id, s.spell_name, SUM(qc.times_cast) AS total_casts
    FROM quests q
    JOIN quest_casts qc ON q.quest_id = qc.quest_id
    JOIN spells s ON qc.spell_id = s.spell_id
    GROUP BY q.wizard_id, s.spell_name
),
ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY wizard_id ORDER BY total_casts DESC, spell_name) AS rn
    FROM casts
)
SELECT r.wizard_id, w.name, r.spell_name, r.total_casts
FROM ranked r JOIN wizards w ON r.wizard_id = w.wizard_id
WHERE r.rn = 1
ORDER BY r.wizard_id;""",
    },
    {
        "id": 28,
        "topic": "Subqueries & CTEs",
        "difficulty": "Hard",
        "title": "Recursive CTE – Full Mentor Chain",
        "question": "Using a recursive CTE, show each wizard's full mentorship depth (how many mentors deep they are from a self-taught root).",
        "hint": "WITH RECURSIVE, anchor = wizards with NULL mentor_id (depth 1).",
        "answer": """WITH RECURSIVE chain AS (
    SELECT wizard_id, name, mentor_id, 1 AS depth
    FROM wizards
    WHERE mentor_id IS NULL
    UNION ALL
    SELECT w.wizard_id, w.name, w.mentor_id, c.depth + 1
    FROM wizards w
    JOIN chain c ON w.mentor_id = c.wizard_id
)
SELECT wizard_id, name, depth
FROM chain
ORDER BY depth, wizard_id;""",
    },

    # ═══════════════ Strings, Dates & Sets ═══════════════
    {
        "id": 29,
        "topic": "Strings, Dates & Sets",
        "difficulty": "Medium",
        "title": "String Functions – First Name & Initials",
        "question": "From wizards, extract each wizard's first name (before the space) and their two-letter initials (e.g. 'Zara Emberveil' → 'ZE').",
        "hint": "SPLIT_PART / UPPER / SUBSTRING. In DuckDB, split_part(name,' ',1).",
        "answer": """SELECT name,
       SPLIT_PART(name, ' ', 1) AS first_name,
       UPPER(SUBSTRING(SPLIT_PART(name, ' ', 1), 1, 1) ||
             SUBSTRING(SPLIT_PART(name, ' ', 2), 1, 1)) AS initials
FROM wizards
ORDER BY wizard_id;""",
    },
    {
        "id": 30,
        "topic": "Strings, Dates & Sets",
        "difficulty": "Medium",
        "title": "Date Functions – Quests per Month",
        "question": "Count how many quests happened in each calendar month of 1023. Show month number and quest count.",
        "hint": "MONTH(quest_date) or EXTRACT(MONTH FROM ...).",
        "answer": """SELECT EXTRACT(MONTH FROM CAST(quest_date AS DATE)) AS month_num,
       COUNT(*) AS quest_count
FROM quests
GROUP BY month_num
ORDER BY month_num;""",
    },
    {
        "id": 31,
        "topic": "Strings, Dates & Sets",
        "difficulty": "Medium",
        "title": "Set Operations – Houses With & Without Quests",
        "question": "Show houses that have at least one wizard who completed a quest, EXCEPT houses whose wizards only ever failed or abandoned quests.",
        "hint": "Use EXCEPT between two house sets (completed vs non-completed-only).",
        "answer": """SELECT DISTINCT w.house
FROM wizards w JOIN quests q ON w.wizard_id = q.wizard_id
WHERE q.status = 'completed'
EXCEPT
SELECT w.house
FROM wizards w JOIN quests q ON w.wizard_id = q.wizard_id
GROUP BY w.house
HAVING COUNT(*) FILTER (WHERE q.status = 'completed') = 0
ORDER BY house;""",
    },

    # ═══════════════ Interview Combo ═══════════════
    {
        "id": 32,
        "topic": "Interview Combo",
        "difficulty": "Hard",
        "title": "Gold Rank per House",
        "question": "Rank wizards within their house by total completed-quest gold. Show house, name, gold, and rank.",
        "hint": "CTE for gold, then RANK() OVER (PARTITION BY house ORDER BY gold DESC).",
        "answer": """WITH wiz_gold AS (
    SELECT w.wizard_id, w.name, w.house,
           ROUND(SUM(qc.times_cast * s.mana_cost * (1 - COALESCE(q.guild_cut_pct,0)/100.0)), 2) AS gold
    FROM wizards w
    JOIN quests q ON w.wizard_id = q.wizard_id
    JOIN quest_casts qc ON q.quest_id = qc.quest_id
    JOIN spells s ON qc.spell_id = s.spell_id
    WHERE q.status = 'completed'
    GROUP BY w.wizard_id, w.name, w.house
)
SELECT house, name, gold,
       RANK() OVER (PARTITION BY house ORDER BY gold DESC) AS house_rank
FROM wiz_gold
ORDER BY house, house_rank;""",
    },
    {
        "id": 33,
        "topic": "Interview Combo",
        "difficulty": "Hard",
        "title": "Guild Hierarchy – Grand-Manager Chain",
        "question": "Show each guild member with their manager's name and their manager's manager's name (2 levels up).",
        "hint": "Double self-join on guild.",
        "answer": """SELECT g.name AS member,
       m.name AS manager,
       mm.name AS grand_manager
FROM guild g
LEFT JOIN guild m ON g.manager_id = m.member_id
LEFT JOIN guild mm ON m.manager_id = mm.member_id
ORDER BY g.member_id;""",
    },
    {
        "id": 34,
        "topic": "Interview Combo",
        "difficulty": "Hard",
        "title": "Month-over-Month Growth % per Wizard",
        "question": "Show each wizard's monthly gold alongside the previous month's gold and the percentage change.",
        "hint": "LAG partitioned by wizard, guard divide-by-zero with NULLIF.",
        "answer": """SELECT wizard_id, month, gold_earned,
       LAG(gold_earned) OVER (PARTITION BY wizard_id ORDER BY month) AS prev_gold,
       ROUND(
           (gold_earned - LAG(gold_earned) OVER (PARTITION BY wizard_id ORDER BY month))
           / NULLIF(LAG(gold_earned) OVER (PARTITION BY wizard_id ORDER BY month), 0) * 100
       , 2) AS pct_change
FROM realm_metrics
ORDER BY wizard_id, month;""",
    },
]
