import pandas as pd
import os
import random

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════
#  🧙 SQL SPELLFORGE ACADEMY  — a magic-RPG world to practice SQL on
#
#  wizards       → the students (self-referential mentors, NULL realms)
#  spells        → castable spells (the "catalog", have a mana_cost)
#  quests        → quests a wizard undertakes (status + guild_cut_pct)
#  quest_casts   → which spells were cast (and how many times) per quest
#  guild         → the ranked guild hierarchy (manager chain)
#  realm_metrics → monthly gold / monsters slain (time-series windows)
#
#  Gold earned on a quest  =  times_cast × mana_cost × (1 - guild_cut/100)
#  Deliberate edge cases: NULL realms, NULL guild_cut, wizards with no
#  quests, failed/abandoned quests, tied power levels, orphan mentors.
# ══════════════════════════════════════════════════════════════════

# ── Wizards (self-join for mentors; NULLs for join edge cases) ──
wizards = pd.DataFrame({
    "wizard_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "name": ["Zara Emberveil", "Kael Frostborn", "Lyra Starweaver", "Doran Ashfell",
             "Nyx Shadowmere", "Orin Brightwood", "Sable Thornquist", "Vex Ironmoon",
             "Mira Duskbloom", "Rowan Stormcaller", "Thea Voidwhisper", "Cassius Grim"],
    "house": ["Emberfall", "Frostspire", "Starweave", "Emberfall", "Voidwatch",
              "Starweave", "Frostspire", "Voidwatch", "Emberfall", "Frostspire",
              "Voidwatch", "Starweave"],
    # home_realm intentionally has NULLs (wanderers with no fixed realm)
    "home_realm": ["Pyrelands", "Glaciern", "Astra", "Pyrelands", None,
                   "Astra", "Glaciern", None, "Pyrelands", "Glaciern", None, "Astra"],
    "tier": ["Archmage", "Adept", "Archmage", "Adept", "Novice", "Mystic", "Adept",
             "Archmage", "Mystic", "Novice", "Adept", "Novice"],
    "enrolled_date": ["1023-01-15", "1023-02-20", "1023-01-10", "1023-03-05",
                      "1023-04-12", "1023-05-01", "1023-06-18", "1023-02-28",
                      "1023-07-22", "1023-08-10", "1023-09-03", "1023-10-19"],
    # mentor_id → self-reference; some wizards are self-taught (NULL)
    "mentor_id": [None, 1, None, 2, 3, None, 4, 1, 3, 5, 8, None],
})

# ── Spells (the castable "catalog"; mana_cost drives gold earned) ──
spells = pd.DataFrame({
    "spell_id": [101, 102, 103, 104, 105, 106, 107, 108],
    "spell_name": ["Ember Lance", "Cinder Storm", "Frost Nova", "Glacial Spear",
                   "Arcane Bolt", "Void Rift", "Soul Harvest", "Mana Shield"],
    "school": ["Pyromancy", "Pyromancy", "Cryomancy", "Cryomancy",
               "Arcane", "Arcane", "Necromancy", "Abjuration"],
    "mana_cost": [25.00, 45.00, 30.00, 60.00, 15.00, 120.00, 200.00, 10.00],
    "discovered_date": ["1018-06-01", "1019-09-15", "1020-01-01", "1021-03-01",
                        "1015-01-01", "1022-11-11", "1017-10-31", "1010-01-01"],
})

# ── Quests (some wizards have none; some have NULL guild_cut) ──
quests = pd.DataFrame({
    "quest_id": list(range(1001, 1031)),
    "wizard_id": [1, 1, 2, 3, 3, 3, 4, 5, 6, 6, 7, 7, 7, 8, 9,
                  10, 10, 1, 2, 4, 5, 6, 8, 9, 10, 3, 4, 7, 1, 2],
    "quest_date": [
        "1023-01-20", "1023-03-15", "1023-02-25", "1023-01-18", "1023-04-10",
        "1023-06-30", "1023-03-12", "1023-05-01", "1023-05-10", "1023-07-20",
        "1023-06-25", "1023-08-05", "1023-09-15", "1023-03-05", "1023-08-01",
        "1023-08-15", "1023-09-20", "1023-10-05", "1023-10-15", "1023-11-01",
        "1023-11-10", "1023-11-20", "1023-12-01", "1023-12-10", "1023-12-20",
        "1023-07-04", "1023-09-09", "1023-10-31", "1023-11-25", "1023-12-15",
    ],
    "status": [
        "completed", "completed", "completed", "completed", "completed",
        "completed", "completed", "abandoned", "completed", "completed",
        "completed", "completed", "failed", "completed", "completed",
        "completed", "completed", "completed", "abandoned", "completed",
        "completed", "completed", "completed", "completed", "completed",
        "failed", "completed", "completed", "completed", "abandoned",
    ],
    # guild_cut_pct → the guild's cut of the loot; NULLs = uncharted quests
    "guild_cut_pct": [
        0, 10, 0, 5, 5, 0, None, 0, 15, 0, 0, 10, 0, None, 0,
        5, 0, 20, None, 0, 0, 10, 0, 5, 0, 0, None, 10, 5, 0,
    ],
})

# ── Quest Casts (which spells were cast per quest, and how often) ──
quest_casts = pd.DataFrame({
    "cast_id": list(range(1, 61)),
    "quest_id": [
        1001, 1001, 1002, 1003, 1004, 1004, 1005, 1006, 1006, 1007,
        1008, 1009, 1009, 1010, 1011, 1012, 1012, 1013, 1014, 1015,
        1016, 1016, 1017, 1018, 1018, 1019, 1020, 1021, 1022, 1022,
        1023, 1024, 1024, 1025, 1025, 1001, 1003, 1007, 1011, 1015,
        1026, 1026, 1027, 1027, 1028, 1028, 1029, 1029, 1030, 1030,
        1005, 1010, 1012, 1017, 1020, 1023, 1026, 1029, 1013, 1018,
    ],
    "spell_id": [
        101, 102, 103, 101, 102, 104, 101, 103, 105, 104,
        106, 101, 102, 103, 105, 101, 106, 104, 102, 103,
        101, 105, 102, 103, 104, 106, 101, 102, 103, 105,
        104, 101, 106, 102, 103, 101, 105, 106, 101, 104,
        107, 108, 101, 103, 105, 102, 106, 104, 108, 107,
        105, 106, 101, 104, 103, 102, 108, 101, 105, 107,
    ],
    "times_cast": [
        2, 1, 1, 3, 2, 1, 4, 1, 2, 1,
        3, 5, 1, 2, 1, 2, 1, 1, 3, 1,
        4, 2, 1, 2, 1, 1, 3, 2, 1, 3,
        1, 4, 2, 2, 1, 1, 1, 2, 3, 1,
        1, 2, 3, 1, 2, 1, 1, 2, 1, 1,
        2, 1, 1, 3, 2, 1, 1, 2, 1, 1,
    ],
})

# ── Guild (ranked hierarchy for self-join / manager-chain problems) ──
guild = pd.DataFrame({
    "member_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "name": ["Grandmaster Vale", "Master Ignus", "Master Sonja", "Warden Bram",
             "Warden Elke", "Acolyte Pip", "Acolyte Rune", "Acolyte Dax"],
    "manager_id": [None, 1, 1, 2, 3, 4, 4, 5],
    "guild_hall": ["Council", "Pyromancy", "Cryomancy", "Pyromancy",
                   "Cryomancy", "Pyromancy", "Pyromancy", "Cryomancy"],
    # power_level has deliberate ties (Master Ignus == Master Sonja) for RANK vs DENSE_RANK
    "power_level": [9800, 7200, 7200, 5100, 5400, 3100, 3100, 2900],
})

# ── Realm Metrics (monthly gold / monsters for window functions) ──
rows = []
for wid in [1, 2, 3]:
    for m in range(1, 13):
        random.seed(wid * 100 + m)
        rows.append({
            "wizard_id": wid,
            "month": f"1023-{m:02d}-01",
            "gold_earned": round(random.uniform(500, 5000), 2),
            "monsters_slain": random.randint(0, 40),
        })
realm_metrics = pd.DataFrame(rows)

# ── Save all CSVs ──
for name, df in [
    ("wizards", wizards),
    ("spells", spells),
    ("quests", quests),
    ("quest_casts", quest_casts),
    ("guild", guild),
    ("realm_metrics", realm_metrics),
]:
    df.to_csv(os.path.join(DATA_DIR, f"{name}.csv"), index=False)
    print(f"Created {name}.csv  ({len(df)} rows)")

print("\n🧙 All Spellforge Academy data generated in", DATA_DIR)
