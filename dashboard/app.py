import streamlit as st
import sqlite3

st.title("Backup & Disaster Recovery Dashboard")

conn = sqlite3.connect("database/backups.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM backups")
rows = cursor.fetchall()

st.subheader("Backup History")

for row in rows:
    st.write(row)

st.metric(
    label="Total Backups",
    value=len(rows)
)

conn.close()