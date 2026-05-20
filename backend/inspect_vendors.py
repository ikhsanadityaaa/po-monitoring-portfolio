import sqlite3

DB_PATH = "po-monitoring-portfolio/backend/instance/po_database.db"
SEARCH_TERMS = ["HLI", "GREEN", "HALE", "INTERNATIONAL", "INDONESIA"]

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

tables = [row[0] for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

for table in tables:
    columns = cur.execute(f'PRAGMA table_info("{table}")').fetchall()
    vendor_columns = [
        col[1]
        for col in columns
        if "vendor" in col[1].lower()
        or "supplier" in col[1].lower()
        or "client" in col[1].lower()
        or "customer" in col[1].lower()
        or "op_unit" in col[1].lower()
        or "operation_unit" in col[1].lower()
    ]

    if not vendor_columns:
        continue

    print(f"\nTABLE {table}")
    for column in vendor_columns:
        print(f"  COLUMN {column}")
        try:
            values = cur.execute(
                f'SELECT "{column}", COUNT(*) FROM "{table}" '
                f'WHERE "{column}" IS NOT NULL AND TRIM(CAST("{column}" AS TEXT)) <> "" '
                f'GROUP BY "{column}" ORDER BY COUNT(*) DESC LIMIT 30'
            ).fetchall()
            for value, count in values:
                value_text = str(value)
                marker = ""
                if any(term.lower() in value_text.lower() for term in SEARCH_TERMS):
                    marker = "  <== match"
                print(f"    {count:6} | {value_text}{marker}")
        except Exception as exc:
            print(f"    ERROR: {exc}")

con.close()