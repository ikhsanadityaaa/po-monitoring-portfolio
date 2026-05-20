import sqlite3

DB_PATH = "po-monitoring-portfolio/backend/instance/po_database.db"
OLD_PATTERNS = [
    "PT HLI GREEN POWER(BONDED AREA)",
    "HLI GREEN POWER (CONSUMABLE)",
    "PT HLI GREEN POWER",
    "PT HLI Green Power",
    "PT HLI green power",
    "pt hli green power",
    "HLI GREEN POWER",
    "HLI Green Power",
    "hli green power",
]
NEW_NAME = "PT HALE INTERNATIONAL INDONESIA"

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

tables = [row[0] for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables:", tables)

matches = []
updates = 0

for table in tables:
    columns = cur.execute(f'PRAGMA table_info("{table}")').fetchall()
    text_columns = [
        col[1]
        for col in columns
        if any(token in (col[2] or "").upper() for token in ("TEXT", "VARCHAR", "CHAR", "CLOB", "STRING"))
        or not col[2]
    ]

    for column in text_columns:
        for old in OLD_PATTERNS:
            rows = cur.execute(
                f'SELECT COUNT(*) FROM "{table}" WHERE "{column}" LIKE ?',
                (f"%{old}%",),
            ).fetchone()[0]
            if rows:
                matches.append((table, column, old, rows))
                cur.execute(
                    f'UPDATE "{table}" SET "{column}" = REPLACE("{column}", ?, ?) WHERE "{column}" LIKE ?',
                    (old, NEW_NAME, f"%{old}%"),
                )
                updates += cur.rowcount

con.commit()

print("Matches:")
for match in matches:
    print(match)

print("Updated rows operations:", updates)

remaining = []
for table in tables:
    columns = cur.execute(f'PRAGMA table_info("{table}")').fetchall()
    text_columns = [
        col[1]
        for col in columns
        if any(token in (col[2] or "").upper() for token in ("TEXT", "VARCHAR", "CHAR", "CLOB", "STRING"))
        or not col[2]
    ]
    for column in text_columns:
        count = cur.execute(
            f'SELECT COUNT(*) FROM "{table}" WHERE "{column}" LIKE ?',
            ("%HLI GREEN POWER%",),
        ).fetchone()[0]
        if count:
            remaining.append((table, column, count))

print("Remaining HLI GREEN POWER:", remaining)

new_hits = []
for table in tables:
    columns = cur.execute(f'PRAGMA table_info("{table}")').fetchall()
    text_columns = [
        col[1]
        for col in columns
        if any(token in (col[2] or "").upper() for token in ("TEXT", "VARCHAR", "CHAR", "CLOB", "STRING"))
        or not col[2]
    ]
    for column in text_columns:
        count = cur.execute(
            f'SELECT COUNT(*) FROM "{table}" WHERE "{column}" LIKE ?',
            (f"%{NEW_NAME}%",),
        ).fetchone()[0]
        if count:
            new_hits.append((table, column, count))

print("New name hits:", new_hits)
con.close()