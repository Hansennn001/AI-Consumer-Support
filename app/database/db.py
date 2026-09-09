import sqlite3


DB_NAME = "database/support.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    # Main support logging table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS support_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_id TEXT,

            email TEXT,

            category TEXT,

            risk_level TEXT,

            risk_reason TEXT,

            response TEXT,

            requires_human BOOLEAN,

            request_id TEXT,

            conversation_id TEXT,

            status TEXT,

            processing_time REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )


    # Conversation memory table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversation_memory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_id TEXT,

            conversation_id TEXT,

            user_message TEXT,

            assistant_response TEXT,

            category TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )


    conn.commit()

    conn.close()



def save_log(state):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO support_logs
        (
            customer_id,
            email,
            category,
            risk_level,
            risk_reason,
            response,
            requires_human,
            request_id,
            conversation_id,
            status,
            processing_time
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (

            state["customer_id"],

            state["email"],

            state["category"],

            state["risk_level"],

            state["risk_reason"],

            state["response"],

            state["requires_human"],

            state["request_id"],

            state["conversation_id"],

            state["status"],

            state["processing_time"]

        )
    )


    conn.commit()

    conn.close()



def save_memory(state):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO conversation_memory
        (
            customer_id,
            conversation_id,
            user_message,
            assistant_response,
            category
        )

        VALUES (?, ?, ?, ?, ?)

        """,

        (

            state["customer_id"],

            state["conversation_id"],

            state["email"],

            state["response"],

            state["category"]

        )
    )


    conn.commit()

    conn.close()



def get_memory(customer_id):

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

            user_message,

            assistant_response,

            category,

            created_at


        FROM conversation_memory


        WHERE customer_id = ?


        ORDER BY created_at DESC


        LIMIT 5

        """,

        (customer_id,)

    )


    rows = cursor.fetchall()


    conn.close()


    return [
        dict(row)
        for row in rows
    ]



def get_logs():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

            id,

            customer_id,

            request_id,

            conversation_id,

            email,

            category,

            risk_level,

            risk_reason,

            response,

            requires_human,

            status,

            processing_time,

            created_at


        FROM support_logs


        ORDER BY id DESC

        """
    )


    rows = cursor.fetchall()


    conn.close()


    return [
        dict(row)
        for row in rows
    ]



def get_pending_reviews():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

            id,

            customer_id,

            request_id,

            conversation_id,

            email,

            category,

            risk_level,

            risk_reason,

            response,

            requires_human,

            status,

            processing_time,

            created_at


        FROM support_logs


        WHERE requires_human = 1

        AND status = 'pending_review'


        ORDER BY id DESC

        """
    )


    rows = cursor.fetchall()


    conn.close()


    return [
        dict(row)
        for row in rows
    ]