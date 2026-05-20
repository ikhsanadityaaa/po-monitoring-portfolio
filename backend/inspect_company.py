import sqlite3

con = sqlite3.connect("po-monitoring-portfolio/backend/instance/po_database.db")
cur = con.cursor()

rows = cur.execute(
    """
    SELECT delivery_memo, specification
    FROM so_data
    WHERE delivery_memo LIKE '%HLI GREEN POWER%'
       OR specification LIKE '%HLI GREEN POWER%'
    """
).fetchall()

for row in rows:
    print(row)

con.close()