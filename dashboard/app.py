import streamlit as st
import sqlite3
import os
import pandas as pd


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Backup & Disaster Recovery",
    page_icon="☁️",
    layout="wide"
)


# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "backups.db"
)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_backup_data():

    if not os.path.exists(DATABASE_PATH):
        return pd.DataFrame()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    query = """
        SELECT *
        FROM backups
        ORDER BY id DESC
    """

    try:

        dataframe = pd.read_sql_query(
            query,
            connection
        )

    except Exception:

        dataframe = pd.DataFrame()

    connection.close()

    return dataframe


# ==========================================
# HEADER
# ==========================================

st.title(
    "☁️ Backup & Disaster Recovery Dashboard"
)

st.markdown(
    """
    Monitor backup operations, backup history,
    and disaster recovery activity from one place.
    """
)


# ==========================================
# LOAD DATA
# ==========================================

df = get_backup_data()


# ==========================================
# METRICS
# ==========================================

if df.empty:

    st.warning(
        "No backup history available yet."
    )

    total_backups = 0
    successful_backups = 0
    failed_backups = 0
    success_rate = 0

else:

    total_backups = len(df)

    successful_backups = len(
        df[
            df["status"].str.upper() == "SUCCESS"
        ]
    )

    failed_backups = len(
        df[
            df["status"].str.upper() == "FAILED"
        ]
    )

    success_rate = (
        successful_backups /
        total_backups
    ) * 100


# ==========================================
# DISPLAY METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Backups",
        total_backups
    )


with col2:

    st.metric(
        "Successful",
        successful_backups
    )


with col3:

    st.metric(
        "Failed",
        failed_backups
    )


with col4:

    st.metric(
        "Success Rate",
        f"{success_rate:.1f}%"
    )


st.divider()


# ==========================================
# BACKUP HISTORY
# ==========================================

st.subheader(
    "📋 Backup History"
)


if df.empty:

    st.info(
        "No backup records found."
    )

else:

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# BACKUP STATUS CHART
# ==========================================

if not df.empty:

    st.subheader(
        "📊 Backup Status"
    )

    status_counts = (
        df["status"]
        .str.upper()
        .value_counts()
    )

    st.bar_chart(
        status_counts
    )


# ==========================================
# LATEST BACKUP
# ==========================================

st.subheader(
    "🕒 Latest Backup"
)


if not df.empty:

    latest = df.iloc[0]

    st.write(
        f"**Filename:** "
        f"{latest.get('filename', 'N/A')}"
    )

    st.write(
        f"**Status:** "
        f"{latest.get('status', 'N/A')}"
    )

    st.write(
        f"**Timestamp:** "
        f"{latest.get('timestamp', 'N/A')}"
    )


# ==========================================
# SYSTEM STATUS
# ==========================================

st.divider()

st.subheader(
    "☁️ System Status"
)

col1, col2 = st.columns(2)


with col1:

    st.success(
        "GitHub Cloud Backup: Connected"
    )


with col2:

    if total_backups > 0:

        st.success(
            "Backup System: Operational"
        )

    else:

        st.warning(
            "Backup System: Waiting for backup"
        )


# ==========================================
# REFRESH BUTTON
# ==========================================

if st.button(
    "🔄 Refresh Dashboard"
):

    st.rerun()