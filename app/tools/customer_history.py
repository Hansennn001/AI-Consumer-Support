import sqlite3
from datetime import datetime, timedelta


DB_NAME = "database/support.db"



def get_recent_contact_count(customer_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    seven_days_ago = (
        datetime.now()
        -
        timedelta(days=7)
    )


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM support_logs
        WHERE customer_id = ?
        AND created_at >= ?
        """,
        (
            customer_id,
            seven_days_ago
        )
    )


    result = cursor.fetchone()


    conn.close()


    return result[0]