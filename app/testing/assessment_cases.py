import uuid
import sqlite3

from datetime import datetime, timedelta

from app.agents.customer_agent import customer_agent


DB_NAME = "database/support.db"



# ======================================================
# STATE BUILDER
# ======================================================

def create_state(customer_id, message):

    return {

        "request_id": str(uuid.uuid4()),

        "conversation_id": str(uuid.uuid4()),

        "customer_id": customer_id,

        "email": message,


        "conversation_history": [],


        "category": "",

        "risk_level": "",

        "risk_reason": "",

        "contact_count": 0,


        "use_tool": False,

        "tool_name": "",

        "tool_query": "",

        "tool_result": "",


        "response": "",

        "requires_human": False,

        "status": "",

        "processing_time": 0.0

    }



def run_agent(customer_id, message):

    state = create_state(
        customer_id,
        message
    )

    return customer_agent.invoke(state)



# ======================================================
# DATABASE CLEANUP
# ======================================================

def cleanup_customer(customer_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM support_logs
        WHERE customer_id = ?
        """,
        (customer_id,)
    )


    cursor.execute(
        """
        DELETE FROM conversation_memory
        WHERE customer_id = ?
        """,
        (customer_id,)
    )


    conn.commit()

    conn.close()



# ======================================================
# TEST 1
# SECURITY BREACH
# ======================================================

def test_security_breach():

    result = run_agent(
        "TEST_SECURITY",
        "My account was hacked"
    )


    assert result["category"] == "security_breach"


    assert result["requires_human"] is True


    assert result["status"] == "pending_review"


    assert (
        "security breach"
        in result["risk_reason"]
    )


    return result



# ======================================================
# TEST 2
# DATA LOSS
# ======================================================

def test_data_loss():

    result = run_agent(
        "TEST_DATA_LOSS",
        "All my files disappeared"
    )


    assert result["category"] == "data_loss"


    assert result["requires_human"] is True


    assert result["status"] == "pending_review"


    assert (
        "data loss"
        in result["risk_reason"]
    )


    return result



# ======================================================
# TEST 3
# SERVICE OUTAGE
# ======================================================

def test_service_outage():

    result = run_agent(
        "TEST_OUTAGE",
        "The service is down and unavailable"
    )


    assert result["category"] == "service_outage"


    assert result["requires_human"] is True


    assert result["status"] == "pending_review"


    assert (
        "service outage"
        in result["risk_reason"]
    )


    return result



# ======================================================
# TEST 4
# CUSTOMER CONTACT > 3 TIMES / 7 DAYS
# ======================================================

def insert_customer_history(customer_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    for i in range(4):

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
            processing_time,
            created_at
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            """,

            (

                customer_id,

                f"Previous request {i+1}",

                "general",

                "low",

                "",

                "Previous response",

                False,

                str(uuid.uuid4()),

                str(uuid.uuid4()),

                "completed",

                0.1,

                datetime.now()
                -
                timedelta(days=i)

            )
        )


    conn.commit()

    conn.close()



def test_customer_history():

    customer_id = "TEST_HISTORY"


    cleanup_customer(customer_id)


    insert_customer_history(
        customer_id
    )


    result = run_agent(

        customer_id,

        "I need help with my account"

    )


    assert result["contact_count"] > 3


    assert result["requires_human"] is True


    assert result["status"] == "pending_review"


    assert (
        "customer contacted support more than 3 times"
        in result["risk_reason"]
    )


    return result



# ======================================================
# TEST 5
# REFUND RAG
# ======================================================

def test_refund_rag():

    result = run_agent(

        "TEST_REFUND",

        "How long does refund take?"

    )


    assert result["category"] == "refund"


    assert result["use_tool"] is False


    assert result["requires_human"] is False


    assert len(result["response"]) > 0


    return result



# ======================================================
# TEST 6
# TAVILY TOOL DECISION
# ======================================================

def test_tool_decision():

    result = run_agent(

        "TEST_TOOL",

        "Is AWS experiencing downtime today?"

    )


    assert result["use_tool"] is True


    assert result["tool_name"] == "tavily"


    return result



# ======================================================
# TEST 7
# CONVERSATION MEMORY
# DATABASE BASED
# ======================================================

def test_memory():

    customer_id = "TEST_MEMORY"


    cleanup_customer(customer_id)



    # Conversation 1
    first_result = run_agent(

        customer_id,

        "My name is Alex How long does refund take?"

    )


    assert first_result["status"] == "completed"



    # Conversation 2
    second_result = run_agent(

        customer_id,

        "What is my name and what was my previous issue?"

    )


    history = second_result.get(
        "conversation_history",
        []
    )


    assert len(history) > 0



    found_previous_context = False


    for item in history:

        previous_message = (

            item["user_message"]
            .lower()

        )


        if (

            "alex"
            in previous_message

            and

            "refund"
            in previous_message

        ):

            found_previous_context = True



    assert found_previous_context is True


    return second_result