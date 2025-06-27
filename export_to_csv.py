import sqlite3
import csv

conn = sqlite3.connect("moderation.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM moderation_events")
rows = cursor.fetchall()

# Fetch column names
col_names = [description[0] for description in cursor.description]

with open("moderation_events_export.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(col_names)
    writer.writerows(rows)

print("Exported moderation_events to moderation_events_export.csv")